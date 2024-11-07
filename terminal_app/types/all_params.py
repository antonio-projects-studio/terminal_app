from __future__ import annotations

__all__ = ["AllParams"]

from collections import UserDict
from typing import Any, overload, Literal


class AllParams(UserDict):

    def __init__(self, mapping=None, /, **kwargs):
        if mapping is not None:
            mapping = {key: value for key, value in mapping.items()}
        else:
            mapping = {}
        if kwargs:
            mapping.update(kwargs)
        super().__init__(mapping)
        self["all_params"] = self

    def __setitem__(self, key: Any, item: Any) -> None:
        if key == "all_params":
            item = self

        return super().__setitem__(key, item)

    @overload
    def __getitem__(self, key: Literal["all_params"]) -> AllParams:
        pass

    @overload
    def __getitem__(self, key: Any) -> Any:
        pass

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)
