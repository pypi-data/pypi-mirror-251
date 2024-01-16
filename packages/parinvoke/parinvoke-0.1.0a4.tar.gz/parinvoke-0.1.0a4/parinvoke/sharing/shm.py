# This file is part of parinvoke.
# Copyright (C) 2020-2023 Boise State University
# Copyright (C) 2023-2024 Drexel University
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import multiprocessing.shared_memory as shm
import pickle
import sys
from typing import Any, NamedTuple, Optional, TypeVar

from . import PersistedModel, sharing_mode

# we have encountered a number of bugs on Windows
SHM_AVAILABLE = sys.platform != "win32"

_log = logging.getLogger(__name__)
T = TypeVar("T")


class SHMBlock(NamedTuple):
    start: int
    end: int


def persist_shm(model: T) -> SHMPersisted[T]:
    """
    Persist a model using :mod:`multiprocessing.shared_memory`.

    Args:
        model: The model to persist.

    Returns:
        PersistedModel: The persisted object.
    """

    buffers: list[pickle.PickleBuffer] = []

    with sharing_mode():
        data = pickle.dumps(model, protocol=5, buffer_callback=buffers.append)

    total_size = sum(memoryview(b).nbytes for b in buffers)
    _log.info(
        "serialized %s to %d pickle bytes with %d buffers of %d bytes",
        model,
        len(data),
        len(buffers),
        total_size,
    )

    if buffers:
        # blit the buffers to the SHM block
        _log.debug("preparing to share %d buffers", len(buffers))
        memory = shm.SharedMemory(create=True, size=total_size)
        cur_offset = 0
        blocks: list[SHMBlock] = []
        for i, buf in enumerate(buffers):
            ba = buf.raw()
            blen = ba.nbytes
            bend = cur_offset + blen
            _log.debug("saving %d bytes in buffer %d/%d", blen, i + 1, len(buffers))
            memory.buf[cur_offset:bend] = ba
            blocks.append(SHMBlock(cur_offset, bend))
            cur_offset = bend
    else:
        memory = None
        blocks = []

    return SHMPersisted[T](data, memory, blocks)


class SHMPersisted(PersistedModel[T]):
    pickle_data: bytes
    blocks: list[SHMBlock]
    memory: Optional[shm.SharedMemory] = None
    shm_name: str | None = None
    _model: Optional[T] = None

    def __init__(self, data: bytes, memory: shm.SharedMemory | None, blocks: list[SHMBlock]):
        self.pickle_data = data
        self.blocks = blocks
        self.memory = memory
        self.shm_name = memory.name if memory is not None else None
        self.is_owner = True

    def get(self):
        if self._model is None:
            _log.debug("loading model from shared memory")
            shm = self._open()
            buffers: list[memoryview] = []
            for bs, be in self.blocks:
                assert shm is not None, "persisted object with blocks has no shared memory"
                buffers.append(shm.buf[bs:be])

            self._model = pickle.loads(self.pickle_data, buffers=buffers)

        return self._model

    def close(self, unlink: bool = True):
        self._model = None

        _log.debug("releasing SHM buffers")
        if self.memory is not None:
            self.memory.close()
            if unlink and self.is_owner and self.is_owner != "transfer":
                self.memory.unlink()
                self.is_owner = False
            self.memory = None

    def _open(self) -> shm.SharedMemory | None:
        if self.shm_name and not self.memory:
            self.memory = shm.SharedMemory(name=self.shm_name)
        return self.memory

    def __getstate__(self):
        return {
            "pickle_data": self.pickle_data,
            "blocks": self.blocks,
            "shm_name": self.shm_name,
            "is_owner": True if self.is_owner == "transfer" else False,
        }

    def __setstate__(self, state: dict[str, Any]):
        self.__dict__.update(state)
        if self.is_owner:
            _log.debug("opening shared buffers after ownership transfer")
            self._open()

    def __del__(self):
        self.close(False)
