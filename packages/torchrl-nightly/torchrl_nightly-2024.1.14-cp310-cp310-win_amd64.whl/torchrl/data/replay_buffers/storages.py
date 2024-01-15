# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import abc
import json
import logging
import os
import textwrap
import warnings
from collections import OrderedDict
from copy import copy
from multiprocessing.context import get_spawning_popen
from pathlib import Path
from typing import Any, Dict, List, Sequence, Union

import numpy as np
import torch
from tensordict import is_tensorclass
from tensordict.memmap import MemmapTensor, MemoryMappedTensor
from tensordict.tensordict import is_tensor_collection, TensorDict, TensorDictBase
from tensordict.utils import _STRDTYPE2DTYPE, expand_right
from torch import multiprocessing as mp

from torchrl._utils import _CKPT_BACKEND, implement_for, VERBOSE
from torchrl.data.replay_buffers.utils import INT_CLASSES

try:
    from torchsnapshot.serialization import tensor_from_memoryview

    _has_ts = True
except ImportError:
    _has_ts = False


class Storage:
    """A Storage is the container of a replay buffer.

    Every storage must have a set, get and __len__ methods implemented.
    Get and set should support integers as well as list of integers.

    The storage does not need to have a definite size, but if it does one should
    make sure that it is compatible with the buffer size.

    """

    def __init__(self, max_size: int) -> None:
        self.max_size = int(max_size)

    @property
    def _attached_entities(self):
        # RBs that use a given instance of Storage should add
        # themselves to this set.
        _attached_entities = self.__dict__.get("_attached_entities_set", None)
        if _attached_entities is None:
            _attached_entities = set()
            self.__dict__["_attached_entities_set"] = _attached_entities
        return _attached_entities

    @abc.abstractmethod
    def set(self, cursor: int, data: Any):
        ...

    @abc.abstractmethod
    def get(self, index: int) -> Any:
        ...

    @abc.abstractmethod
    def dumps(self, path):
        ...

    @abc.abstractmethod
    def loads(self, path):
        ...

    def attach(self, buffer: Any) -> None:
        """This function attaches a sampler to this storage.

        Buffers that read from this storage must be included as an attached
        entity by calling this method. This guarantees that when data
        in the storage changes, components are made aware of changes even if the storage
        is shared with other buffers (eg. Priority Samplers).

        Args:
            buffer: the object that reads from this storage.
        """
        self._attached_entities.add(buffer)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, index, value):
        ret = self.set(index, value)
        for ent in self._attached_entities:
            ent.mark_update(index)
        return ret

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    @abc.abstractmethod
    def __len__(self):
        ...

    @abc.abstractmethod
    def state_dict(self) -> Dict[str, Any]:
        ...

    @abc.abstractmethod
    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        ...

    @abc.abstractmethod
    def _empty(self):
        ...


class ListStorage(Storage):
    """A storage stored in a list.

    Args:
        max_size (int): the maximum number of elements stored in the storage.

    """

    def __init__(self, max_size: int):
        super().__init__(max_size)
        self._storage = []

    def dumps(self, path):
        raise NotImplementedError(
            "ListStorage doesn't support serialization via `dumps` - `loads` API."
        )

    def loads(self, path):
        raise NotImplementedError(
            "ListStorage doesn't support serialization via `dumps` - `loads` API."
        )

    def set(self, cursor: Union[int, Sequence[int], slice], data: Any):
        if not isinstance(cursor, INT_CLASSES):
            if (isinstance(cursor, torch.Tensor) and cursor.numel() <= 1) or (
                isinstance(cursor, np.ndarray) and cursor.size <= 1
            ):
                self.set(int(cursor), data)
                return
            if isinstance(cursor, slice):
                self._storage[cursor] = data
                return
            for _cursor, _data in zip(cursor, data):
                self.set(_cursor, _data)
            return
        else:
            if cursor > len(self._storage):
                raise RuntimeError(
                    "Cannot append data located more than one item away from "
                    f"the storage size: the storage size is {len(self)} "
                    f"and the index of the item to be set is {cursor}."
                )
            if cursor >= self.max_size:
                raise RuntimeError(
                    f"Cannot append data to the list storage: "
                    f"maximum capacity is {self.max_size} "
                    f"and the index of the item to be set is {cursor}."
                )
            if cursor == len(self._storage):
                self._storage.append(data)
            else:
                self._storage[cursor] = data

    def get(self, index: Union[int, Sequence[int], slice]) -> Any:
        if isinstance(index, (INT_CLASSES, slice)):
            return self._storage[index]
        else:
            return [self._storage[i] for i in index]

    def __len__(self):
        return len(self._storage)

    def state_dict(self) -> Dict[str, Any]:
        return {
            "_storage": [
                elt if not hasattr(elt, "state_dict") else elt.state_dict()
                for elt in self._storage
            ]
        }

    def load_state_dict(self, state_dict):
        _storage = state_dict["_storage"]
        self._storage = []
        for elt in _storage:
            if isinstance(elt, torch.Tensor):
                self._storage.append(elt)
            elif isinstance(elt, (dict, OrderedDict)):
                self._storage.append(TensorDict({}, []).load_state_dict(elt))
            else:
                raise TypeError(
                    f"Objects of type {type(elt)} are not supported by ListStorage.load_state_dict"
                )

    def _empty(self):
        self._storage = []

    def __getstate__(self):
        if get_spawning_popen() is not None:
            raise RuntimeError(
                f"Cannot share a storage of type {type(self)} between processes."
            )
        state = copy(self.__dict__)
        return state


class TensorStorage(Storage):
    """A storage for tensors and tensordicts.

    Args:
        storage (tensor or TensorDict): the data buffer to be used.
        max_size (int): size of the storage, i.e. maximum number of elements stored
            in the buffer.
        device (torch.device, optional): device where the sampled tensors will be
            stored and sent. Default is :obj:`torch.device("cpu")`.
            If "auto" is passed, the device is automatically gathered from the
            first batch of data passed. This is not enabled by default to avoid
            data placed on GPU by mistake, causing OOM issues.

    Examples:
        >>> data = TensorDict({
        ...     "some data": torch.randn(10, 11),
        ...     ("some", "nested", "data"): torch.randn(10, 11, 12),
        ... }, batch_size=[10, 11])
        >>> storage = TensorStorage(data)
        >>> len(storage)  # only the first dimension is considered as indexable
        10
        >>> storage.get(0)
        TensorDict(
            fields={
                some data: Tensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
                some: TensorDict(
                    fields={
                        nested: TensorDict(
                            fields={
                                data: Tensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False)},
                            batch_size=torch.Size([11]),
                            device=None,
                            is_shared=False)},
                    batch_size=torch.Size([11]),
                    device=None,
                    is_shared=False)},
            batch_size=torch.Size([11]),
            device=None,
            is_shared=False)
        >>> storage.set(0, storage.get(0).zero_()) # zeros the data along index ``0``

    This class also supports tensorclass data.

    Examples:
        >>> from tensordict import tensorclass
        >>> @tensorclass
        ... class MyClass:
        ...     foo: torch.Tensor
        ...     bar: torch.Tensor
        >>> data = MyClass(foo=torch.randn(10, 11), bar=torch.randn(10, 11, 12), batch_size=[10, 11])
        >>> storage = TensorStorage(data)
        >>> storage.get(0)
        MyClass(
            bar=Tensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False),
            foo=Tensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
            batch_size=torch.Size([11]),
            device=None,
            is_shared=False)

    """

    @classmethod
    def __new__(cls, *args, **kwargs):
        cls._storage = None
        return super().__new__(cls)

    def __init__(self, storage, max_size=None, device="cpu"):
        if not ((storage is None) ^ (max_size is None)):
            if storage is None:
                raise ValueError("Expected storage to be non-null.")
            if max_size != storage.shape[0]:
                raise ValueError(
                    "The max-size and the storage shape mismatch: got "
                    f"max_size={max_size} for a storage of shape {storage.shape}."
                )
        elif storage is not None:
            max_size = storage.shape[0]
        super().__init__(max_size)
        self.initialized = storage is not None
        if self.initialized:
            self._len = max_size
        else:
            self._len = 0
        self.device = (
            torch.device(device)
            if device != "auto"
            else storage.device
            if storage is not None
            else "auto"
        )
        self._storage = storage

    def dumps(self, path):
        path = Path(path)
        path.mkdir(exist_ok=True)

        if not self.initialized:
            raise RuntimeError("Cannot save a non-initialized storage.")
        if isinstance(self._storage, torch.Tensor):
            try:
                MemoryMappedTensor.from_filename(
                    shape=self._storage.shape,
                    filename=path / "storage.memmap",
                    dtype=self._storage.dtype,
                ).copy_(self._storage)
            except FileNotFoundError:
                MemoryMappedTensor.from_tensor(
                    self._storage, filename=path / "storage.memmap", copy_existing=True
                )
            is_tensor = True
            dtype = str(self._storage.dtype)
            shape = list(self._storage.shape)
        else:
            # try to load the path and overwrite.
            self._storage.memmap(
                path, copy_existing=True, num_threads=torch.get_num_threads()
            )
            is_tensor = False
            dtype = None
            shape = None

        with open(path / "storage_metadata.json", "w") as file:
            json.dump(
                {
                    "is_tensor": is_tensor,
                    "dtype": dtype,
                    "shape": shape,
                    "len": self._len,
                },
                file,
            )

    def loads(self, path):
        with open(path / "storage_metadata.json", "r") as file:
            metadata = json.load(file)
        is_tensor = metadata["is_tensor"]
        shape = metadata["shape"]
        dtype = metadata["dtype"]
        _len = metadata["len"]
        if dtype is not None:
            shape = torch.Size(shape)
            dtype = _STRDTYPE2DTYPE[dtype]
        if is_tensor:
            _storage = MemoryMappedTensor.from_filename(
                path / "storage.memmap", shape=shape, dtype=dtype
            ).clone()
        else:
            _storage = TensorDict.load_memmap(path)
        if not self.initialized:
            self._storage = _storage
            self.initialized = True
        else:
            self._storage.copy_(_storage)
        self._len = _len

    @property
    def _len(self):
        _len_value = self.__dict__.get("_len_value", None)
        if _len_value is None:
            _len_value = self._len_value = mp.Value("i", 0)
        return _len_value.value

    @_len.setter
    def _len(self, value):
        _len_value = self.__dict__.get("_len_value", None)
        if _len_value is None:
            _len_value = self._len_value = mp.Value("i", 0)
        _len_value.value = value

    def __getstate__(self):
        state = copy(self.__dict__)
        if get_spawning_popen() is None:
            len = self._len
            del state["_len_value"]
            state["len__context"] = len
        elif not self.initialized:
            # check that the storage is initialized
            raise RuntimeError(
                f"Cannot share a storage of type {type(self)} between processed if "
                f"it has not been initialized yet. Populate the buffer with "
                f"some data in the main process before passing it to the other "
                f"subprocesses (or create the buffer explicitely with a TensorStorage)."
            )
        else:
            # check that the content is shared, otherwise tell the user we can't help
            storage = self._storage
            STORAGE_ERR = "The storage must be place in shared memory or memmapped before being shared between processes."
            if is_tensor_collection(storage):
                if not storage.is_memmap() and not storage.is_shared():
                    raise RuntimeError(STORAGE_ERR)
            else:
                if (
                    not isinstance(storage, MemoryMappedTensor)
                    and not storage.is_shared()
                ):
                    raise RuntimeError(STORAGE_ERR)

        return state

    def __setstate__(self, state):
        len = state.pop("len__context", None)
        if len is not None:
            _len_value = mp.Value("i", len)
            state["_len_value"] = _len_value
        self.__dict__.update(state)

    def state_dict(self) -> Dict[str, Any]:
        _storage = self._storage
        if isinstance(_storage, torch.Tensor):
            pass
        elif is_tensor_collection(_storage):
            _storage = _storage.state_dict()
        elif _storage is None:
            _storage = {}
        else:
            raise TypeError(
                f"Objects of type {type(_storage)} are not supported by {type(self)}.state_dict"
            )
        return {
            "_storage": _storage,
            "initialized": self.initialized,
            "_len": self._len,
        }

    def load_state_dict(self, state_dict):
        _storage = copy(state_dict["_storage"])
        if isinstance(_storage, torch.Tensor):
            if isinstance(self._storage, torch.Tensor):
                self._storage.copy_(_storage)
            elif self._storage is None:
                self._storage = _storage
            else:
                raise RuntimeError(
                    f"Cannot copy a storage of type {type(_storage)} onto another of type {type(self._storage)}"
                )
        elif isinstance(_storage, (dict, OrderedDict)):
            if is_tensor_collection(self._storage):
                self._storage.load_state_dict(_storage)
            elif self._storage is None:
                self._storage = TensorDict({}, []).load_state_dict(_storage)
            else:
                raise RuntimeError(
                    f"Cannot copy a storage of type {type(_storage)} onto another of type {type(self._storage)}"
                )
        else:
            raise TypeError(
                f"Objects of type {type(_storage)} are not supported by ListStorage.load_state_dict"
            )
        self.initialized = state_dict["initialized"]
        self._len = state_dict["_len"]

    @implement_for("torch", "2.0", None)
    def set(
        self,
        cursor: Union[int, Sequence[int], slice],
        data: Union[TensorDictBase, torch.Tensor],
    ):
        if isinstance(cursor, INT_CLASSES):
            self._len = max(self._len, cursor + 1)
        else:
            self._len = max(self._len, max(cursor) + 1)

        if not self.initialized:
            if not isinstance(cursor, INT_CLASSES):
                self._init(data[0])
            else:
                self._init(data)
        self._storage[cursor] = data

    @implement_for("torch", None, "2.0")
    def set(  # noqa: F811
        self,
        cursor: Union[int, Sequence[int], slice],
        data: Union[TensorDictBase, torch.Tensor],
    ):
        if isinstance(cursor, INT_CLASSES):
            self._len = max(self._len, cursor + 1)
        else:
            self._len = max(self._len, max(cursor) + 1)

        if not self.initialized:
            if not isinstance(cursor, INT_CLASSES):
                self._init(data[0])
            else:
                self._init(data)
        if not isinstance(cursor, (*INT_CLASSES, slice)):
            if not isinstance(cursor, torch.Tensor):
                cursor = torch.tensor(cursor, dtype=torch.long)
            elif cursor.dtype != torch.long:
                cursor = cursor.to(dtype=torch.long)
            if len(cursor) > len(self._storage):
                warnings.warn(
                    "A cursor of length superior to the storage capacity was provided. "
                    "To accomodate for this, the cursor will be truncated to its last "
                    "element such that its length matched the length of the storage. "
                    "This may **not** be the optimal behaviour for your application! "
                    "Make sure that the storage capacity is big enough to support the "
                    "batch size provided."
                )
        self._storage[cursor] = data

    @implement_for("torch", None, "2.0")
    def set(  # noqa: F811
        self,
        cursor: Union[int, Sequence[int], slice],
        data: Union[TensorDictBase, torch.Tensor],
    ):
        if isinstance(cursor, INT_CLASSES):
            self._len = max(self._len, cursor + 1)
        else:
            self._len = max(self._len, max(cursor) + 1)

        if not self.initialized:
            if not isinstance(cursor, INT_CLASSES):
                self._init(data[0])
            else:
                self._init(data)
        if not isinstance(cursor, (*INT_CLASSES, slice)):
            if not isinstance(cursor, torch.Tensor):
                cursor = torch.tensor(cursor, dtype=torch.long, device=self.device)
            elif cursor.dtype != torch.long:
                cursor = cursor.to(dtype=torch.long, device=self.device)
            if len(cursor) > len(self._storage):
                warnings.warn(
                    "A cursor of length superior to the storage capacity was provided. "
                    "To accomodate for this, the cursor will be truncated to its last "
                    "element such that its length matched the length of the storage. "
                    "This may **not** be the optimal behaviour for your application! "
                    "Make sure that the storage capacity is big enough to support the "
                    "batch size provided."
                )
        self._storage[cursor] = data

    def get(self, index: Union[int, Sequence[int], slice]) -> Any:
        if self._len < self.max_size:
            storage = self._storage[: self._len]
        else:
            storage = self._storage
        if not self.initialized:
            raise RuntimeError(
                "Cannot get an item from an unitialized LazyMemmapStorage"
            )
        out = storage[index]
        if is_tensor_collection(out):
            out = _reset_batch_size(out)
            return out  # .unlock_()
        return out

    def __len__(self):
        return self._len

    def _empty(self):
        # assuming that the data structure is the same, we don't need to to
        # anything if the cursor is reset to 0
        self._len = 0

    def _init(self):
        raise NotImplementedError(
            f"{type(self)} must be initialized during construction."
        )


class LazyTensorStorage(TensorStorage):
    """A pre-allocated tensor storage for tensors and tensordicts.

    Args:
        max_size (int): size of the storage, i.e. maximum number of elements stored
            in the buffer.
        device (torch.device, optional): device where the sampled tensors will be
            stored and sent. Default is :obj:`torch.device("cpu")`.
            If "auto" is passed, the device is automatically gathered from the
            first batch of data passed. This is not enabled by default to avoid
            data placed on GPU by mistake, causing OOM issues.

    Examples:
        >>> data = TensorDict({
        ...     "some data": torch.randn(10, 11),
        ...     ("some", "nested", "data"): torch.randn(10, 11, 12),
        ... }, batch_size=[10, 11])
        >>> storage = LazyTensorStorage(100)
        >>> storage.set(range(10), data)
        >>> len(storage)  # only the first dimension is considered as indexable
        10
        >>> storage.get(0)
        TensorDict(
            fields={
                some data: Tensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
                some: TensorDict(
                    fields={
                        nested: TensorDict(
                            fields={
                                data: Tensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False)},
                            batch_size=torch.Size([11]),
                            device=cpu,
                            is_shared=False)},
                    batch_size=torch.Size([11]),
                    device=cpu,
                    is_shared=False)},
            batch_size=torch.Size([11]),
            device=cpu,
            is_shared=False)
        >>> storage.set(0, storage.get(0).zero_()) # zeros the data along index ``0``

    This class also supports tensorclass data.

    Examples:
        >>> from tensordict import tensorclass
        >>> @tensorclass
        ... class MyClass:
        ...     foo: torch.Tensor
        ...     bar: torch.Tensor
        >>> data = MyClass(foo=torch.randn(10, 11), bar=torch.randn(10, 11, 12), batch_size=[10, 11])
        >>> storage = LazyTensorStorage(10)
        >>> storage.set(range(10), data)
        >>> storage.get(0)
        MyClass(
            bar=Tensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False),
            foo=Tensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
            batch_size=torch.Size([11]),
            device=cpu,
            is_shared=False)

    """

    def __init__(self, max_size, device="cpu"):
        super().__init__(storage=None, max_size=max_size, device=device)

    def _init(self, data: Union[TensorDictBase, torch.Tensor]) -> None:
        if VERBOSE:
            logging.info("Creating a TensorStorage...")
        if self.device == "auto":
            self.device = data.device
        if isinstance(data, torch.Tensor):
            # if Tensor, we just create a MemoryMappedTensor of the desired shape, device and dtype
            out = torch.empty(
                self.max_size,
                *data.shape,
                device=self.device,
                dtype=data.dtype,
            )
        elif is_tensorclass(data):
            out = (
                data.expand(self.max_size, *data.shape).clone().zero_().to(self.device)
            )
        else:
            out = (
                data.expand(self.max_size, *data.shape)
                .to_tensordict()
                .zero_()
                .clone()
                .to(self.device)
            )

        self._storage = out
        self.initialized = True


class LazyMemmapStorage(LazyTensorStorage):
    """A memory-mapped storage for tensors and tensordicts.

    Args:
        max_size (int): size of the storage, i.e. maximum number of elements stored
            in the buffer.
        scratch_dir (str or path): directory where memmap-tensors will be written.
        device (torch.device, optional): device where the sampled tensors will be
            stored and sent. Default is :obj:`torch.device("cpu")`.
            If ``None`` is provided, the device is automatically gathered from the
            first batch of data passed. This is not enabled by default to avoid
            data placed on GPU by mistake, causing OOM issues.

    Examples:
        >>> data = TensorDict({
        ...     "some data": torch.randn(10, 11),
        ...     ("some", "nested", "data"): torch.randn(10, 11, 12),
        ... }, batch_size=[10, 11])
        >>> storage = LazyMemmapStorage(100)
        >>> storage.set(range(10), data)
        >>> len(storage)  # only the first dimension is considered as indexable
        10
        >>> storage.get(0)
        TensorDict(
            fields={
                some data: MemoryMappedTensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
                some: TensorDict(
                    fields={
                        nested: TensorDict(
                            fields={
                                data: MemoryMappedTensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False)},
                            batch_size=torch.Size([11]),
                            device=cpu,
                            is_shared=False)},
                    batch_size=torch.Size([11]),
                    device=cpu,
                    is_shared=False)},
            batch_size=torch.Size([11]),
            device=cpu,
            is_shared=False)

    This class also supports tensorclass data.

    Examples:
        >>> from tensordict import tensorclass
        >>> @tensorclass
        ... class MyClass:
        ...     foo: torch.Tensor
        ...     bar: torch.Tensor
        >>> data = MyClass(foo=torch.randn(10, 11), bar=torch.randn(10, 11, 12), batch_size=[10, 11])
        >>> storage = LazyMemmapStorage(10)
        >>> storage.set(range(10), data)
        >>> storage.get(0)
        MyClass(
            bar=MemoryMappedTensor(shape=torch.Size([11, 12]), device=cpu, dtype=torch.float32, is_shared=False),
            foo=MemoryMappedTensor(shape=torch.Size([11]), device=cpu, dtype=torch.float32, is_shared=False),
            batch_size=torch.Size([11]),
            device=cpu,
            is_shared=False)

    """

    def __init__(self, max_size, scratch_dir=None, device="cpu"):
        super().__init__(max_size)
        self.initialized = False
        self.scratch_dir = None
        if scratch_dir is not None:
            self.scratch_dir = str(scratch_dir)
            if self.scratch_dir[-1] != "/":
                self.scratch_dir += "/"
        self.device = torch.device(device) if device != "auto" else device
        self._len = 0

    def state_dict(self) -> Dict[str, Any]:
        _storage = self._storage
        if isinstance(_storage, torch.Tensor):
            _storage = _mem_map_tensor_as_tensor(_storage)
        elif isinstance(_storage, TensorDictBase):
            _storage = _storage.apply(_mem_map_tensor_as_tensor).state_dict()
        elif _storage is None:
            _storage = {}
        else:
            raise TypeError(
                f"Objects of type {type(_storage)} are not supported by LazyTensorStorage.state_dict"
            )
        return {
            "_storage": _storage,
            "initialized": self.initialized,
            "_len": self._len,
        }

    def load_state_dict(self, state_dict):
        _storage = copy(state_dict["_storage"])
        if isinstance(_storage, torch.Tensor):
            if isinstance(self._storage, torch.Tensor):
                _mem_map_tensor_as_tensor(self._storage).copy_(_storage)
            elif self._storage is None:
                self._storage = _make_memmap(
                    _storage,
                    path=self.scratch_dir + "/tensor.memmap"
                    if self.scratch_dir is not None
                    else None,
                )
            else:
                raise RuntimeError(
                    f"Cannot copy a storage of type {type(_storage)} onto another of type {type(self._storage)}"
                )
        elif isinstance(_storage, (dict, OrderedDict)):
            if is_tensor_collection(self._storage):
                self._storage.load_state_dict(_storage)
                self._storage.memmap_()
            elif self._storage is None:
                warnings.warn(
                    "Loading the storage on an uninitialized TensorDict."
                    "It is preferable to load a storage onto a"
                    "pre-allocated one whenever possible."
                )
                self._storage = TensorDict({}, []).load_state_dict(_storage)
                self._storage.memmap_()
            else:
                raise RuntimeError(
                    f"Cannot copy a storage of type {type(_storage)} onto another of type {type(self._storage)}"
                )
        else:
            raise TypeError(
                f"Objects of type {type(_storage)} are not supported by ListStorage.load_state_dict"
            )
        self.initialized = state_dict["initialized"]
        self._len = state_dict["_len"]

    def _init(self, data: Union[TensorDictBase, torch.Tensor]) -> None:
        if VERBOSE:
            logging.info("Creating a MemmapStorage...")
        if self.device == "auto":
            self.device = data.device
        if self.device.type != "cpu":
            warnings.warn(
                "Support for Memmap device other than CPU will be deprecated in v0.4.0. "
                "Using a 'cuda' device may be suboptimal.",
                category=DeprecationWarning,
            )
        if is_tensor_collection(data):
            out = data.clone().to(self.device)
            out = out.expand(self.max_size, *data.shape)
            out = out.memmap_like(prefix=self.scratch_dir)

            for key, tensor in sorted(
                out.items(include_nested=True, leaves_only=True), key=str
            ):
                if VERBOSE:
                    filesize = os.path.getsize(tensor.filename) / 1024 / 1024
                    logging.info(
                        f"\t{key}: {tensor.filename}, {filesize} Mb of storage (size: {tensor.shape})."
                    )
        else:
            # If not a tensorclass/tensordict, it must be a tensor(-like)
            # if Tensor, we just create a MemoryMappedTensor of the desired shape, device and dtype
            out = _make_empty_memmap(
                (self.max_size, *data.shape),
                dtype=data.dtype,
                path=self.scratch_dir + "/tensor.memmap"
                if self.scratch_dir is not None
                else None,
            )
            if VERBOSE:
                filesize = os.path.getsize(out.filename) / 1024 / 1024
                logging.info(
                    f"The storage was created in {out.filename} and occupies {filesize} Mb of storage."
                )
        self._storage = out
        self.initialized = True

    def get(self, index: Union[int, Sequence[int], slice]) -> Any:
        result = super().get(index)
        # to be deprecated in v0.4
        if result.device != self.device:
            return result.to(self.device, non_blocking=True)
        return result


class StorageEnsemble(Storage):
    """An ensemble of storages.

    This class is designed to work with :class:`~torchrl.data.replay_buffers.replay_buffers.ReplayBufferEnsemble`.

    Args:
        storages (sequence of Storage): the storages to make the composite storage.

    Keyword Args:
        transforms (list of :class:`~torchrl.envs.Transform`, optional): a list of
            transforms of the same length as storages.

    .. warning::
      This class signatures for :meth:`~.get` does not match other storages, as
      it will return a tuple ``(buffer_id, samples)`` rather than just the samples.

    .. warning::
       This class does not support writing (similarly to :class:`~torchrl.data.replay_buffers.writers.WriterEnsemble`).
       To extend one of the replay buffers, simply index the parent
       :class:`~torchrl.data.ReplayBufferEnsemble` object.

    """

    def __init__(
        self,
        *storages: Storage,
        transforms: List["Transform"] = None,  # noqa: F821
    ):
        self._storages = storages
        self._transforms = transforms
        if transforms is not None and len(transforms) != len(storages):
            raise TypeError(
                "transforms must have the same length as the storages " "provided."
            )

    @property
    def _attached_entities(self):
        return set()

    def extend(self, value):
        raise RuntimeError

    def add(self, value):
        raise RuntimeError

    def get(self, item):
        # we return the buffer id too to be able to track the appropriate collate_fn
        buffer_ids = item.get("buffer_ids")
        index = item.get("index")
        results = []
        for (buffer_id, sample) in zip(buffer_ids, index):
            buffer_id = self._convert_id(buffer_id)
            results.append((buffer_id, self._get_storage(buffer_id).get(sample)))
        if self._transforms is not None:
            results = [
                (buffer_id, self._transforms[buffer_id](result))
                if self._transforms[buffer_id] is not None
                else (buffer_id, result)
                for buffer_id, result in results
            ]
        return results

    def _convert_id(self, sub):
        if isinstance(sub, torch.Tensor):
            sub = sub.item()
        return sub

    def _get_storage(self, sub):
        return self._storages[sub]

    def dumps(self, path: Path):
        path = Path(path).absolute()
        for i, storage in enumerate(self._storages):
            storage.dumps(path / str(i))
        if self._transforms is not None:
            for i, transform in enumerate(self._transforms):
                torch.save(transform.state_dict(), path / f"{i}_transform.pt")

    def loads(self, path: Path):
        path = Path(path).absolute()
        for i, storage in enumerate(self._storages):
            storage.loads(path / str(i))
        if self._transforms is not None:
            for i, transform in enumerate(self._transforms):
                transform.load_state_dict(torch.load(path / f"{i}_transform.pt"))

    def state_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        raise NotImplementedError

    _INDEX_ERROR = "Expected an index of type torch.Tensor, range, np.ndarray, int, slice or ellipsis, got {} instead."

    def __getitem__(self, index):
        if isinstance(index, tuple):
            if index[0] is Ellipsis:
                index = (slice(None), index[1:])
            result = self[index[0]]
            if len(index) > 1:
                if result is self:
                    # then index[0] is an ellipsis/slice(None)
                    sample = [storage[index[1:]] for storage in self._storages]
                    return sample
                if isinstance(result, StorageEnsemble):
                    new_index = (slice(None), *index[1:])
                    return result[new_index]
                return result[index[1:]]
            return result
        if isinstance(index, slice) and index == slice(None):
            return self
        if isinstance(index, (list, range, np.ndarray)):
            index = torch.tensor(index)
        if isinstance(index, torch.Tensor):
            if index.ndim > 1:
                raise RuntimeError(
                    f"Cannot index a {type(self)} with tensor indices that have more than one dimension."
                )
            if index.is_floating_point():
                raise TypeError(
                    "A floating point index was recieved when an integer dtype was expected."
                )
        if isinstance(index, int) or (not isinstance(index, slice) and len(index) == 0):
            try:
                index = int(index)
            except Exception:
                raise IndexError(self._INDEX_ERROR.format(type(index)))
            try:
                return self._storages[index]
            except IndexError:
                raise IndexError(self._INDEX_ERROR.format(type(index)))
        if isinstance(index, torch.Tensor):
            index = index.tolist()
            storages = [self._storages[i] for i in index]
            transforms = (
                [self._transforms[i] for i in index]
                if self._transforms is not None
                else [None] * len(index)
            )
        else:
            # slice
            storages = self._storages[index]
            transforms = (
                self._transforms[index]
                if self._transforms is not None
                else [None] * len(storages)
            )

        return StorageEnsemble(*storages, transforms=transforms)

    def __len__(self):
        return len(self._storages)

    def __repr__(self):
        storages = textwrap.indent(f"storages={self._storages}", " " * 4)
        transforms = textwrap.indent(f"transforms={self._transforms}", " " * 4)
        return f"StorageEnsemble(\n{storages}, \n{transforms})"


# Utils
def _mem_map_tensor_as_tensor(mem_map_tensor: MemmapTensor) -> torch.Tensor:
    if _CKPT_BACKEND == "torchsnapshot" and not _has_ts:
        raise ImportError(
            "the checkpointing backend is set to torchsnapshot but the library is not installed. Consider installing the library or switch to another backend. "
            f"Supported backends are {_CKPT_BACKEND.backends}"
        )
    if isinstance(mem_map_tensor, torch.Tensor):
        # This will account for MemoryMappedTensors
        return mem_map_tensor
    if _CKPT_BACKEND == "torchsnapshot":
        # TorchSnapshot doesn't know how to stream MemmapTensor, so we view MemmapTensor
        # as a Tensor for saving and loading purposes. This doesn't incur any copy.
        return tensor_from_memoryview(
            dtype=mem_map_tensor.dtype,
            shape=list(mem_map_tensor.shape),
            mv=memoryview(mem_map_tensor._memmap_array),
        )
    elif _CKPT_BACKEND == "torch":
        return mem_map_tensor._tensor


def _reset_batch_size(x):
    """Resets the batch size of a tensordict.

    In some cases we save the original shape of the tensordict as a tensor (or memmap tensor).

    This function will read that tensor, extract its items and reset the shape
    of the tensordict to it. If items have an incompatible shape (e.g. "index")
    they will be expanded to the right to match it.

    """
    shape = x.get("_rb_batch_size", None)
    if shape is not None:
        warnings.warn(
            "Reshaping nested tensordicts will be deprecated soon.",
            category=DeprecationWarning,
        )
        data = x.get("_data")
        # we need to reset the batch-size
        if isinstance(shape, MemmapTensor):
            shape = shape.as_tensor()
        locked = data.is_locked
        if locked:
            data.unlock_()
        shape = [s.item() for s in shape[0]]
        shape = torch.Size([x.shape[0], *shape])
        # we may need to update some values in the data
        for key, value in x.items():
            if value.ndim >= len(shape):
                continue
            value = expand_right(value, shape)
            data.set(key, value)
        if locked:
            data.lock_()
        return data
    data = x.get("_data", None)
    if data is not None:
        return data
    return x


def _collate_list_tensordict(x):
    out = torch.stack(x, 0)
    if is_tensor_collection(out):
        return _reset_batch_size(out)
    return out


def _collate_id(x):
    return x


def _get_default_collate(storage, _is_tensordict=False):
    if isinstance(storage, ListStorage):
        if _is_tensordict:
            return _collate_list_tensordict
        else:
            return torch.utils.data._utils.collate.default_collate
    elif isinstance(storage, TensorStorage):
        return _collate_id
    else:
        raise NotImplementedError(
            f"Could not find a default collate_fn for storage {type(storage)}."
        )


def _make_memmap(tensor, path):
    return MemoryMappedTensor.from_tensor(tensor, filename=path)


def _make_empty_memmap(shape, dtype, path):
    return MemoryMappedTensor.empty(shape=shape, dtype=dtype, filename=path)
