# SPDX-License-Identifier: LGPL-3.0-only

import os
from typing import Any, Callable, Union, TypeVar

from fluent.runtime.types import (
    FluentDate,
    FluentDateTime,
    FluentDecimal,
    FluentFloat,
    FluentInt,
    FluentNone,
    FluentNumber,
    FluentType,
)

# re-exports
__all__ = (
    "FluentDate",
    "FluentDateTime",
    "FluentDecimal",
    "FluentFloat",
    "FluentInt",
    "FluentNone",
    "FluentNumber",
    "FluentBool",
    "FluentType",
)


def FluentBool(value: bool) -> str:
    """Transform boolean value to lowercase string."""
    return str(value).lower()


PathT = Union[str, os.PathLike[Any]]
ReturnT = TypeVar("ReturnT", bound = Union[FluentType, str])
FluentFunction = Callable[..., ReturnT]
