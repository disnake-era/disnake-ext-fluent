# SPDX-License-Identifier: LGPL-3.0-only

import os
from typing import Any, Callable, Self, Union, TypeVar
import babel

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
    "FluentText",
    "FluentBool",
    "FluentType",
)


class FluentText(FluentType):
    """Fluent type for raw, non-localizable strings."""

    _inner: str

    def __init__(self: Self, inner: str) -> None:
        self._inner = inner

    def format(self: Self, locale: babel.Locale) -> str:
        return self._inner


class FluentBool(FluentType):
    """Fluent type for booleans."""

    _inner: bool

    def __init__(self: Self, inner: bool) -> None:
        self._inner = inner

    def format(self: Self, locale: babel.Locale) -> str:
        return "true" if self._inner else "false"


PathT = Union[str, os.PathLike[Any]]
ReturnT = TypeVar("ReturnT", bound = FluentType)
FluentFunction = Callable[..., ReturnT]
