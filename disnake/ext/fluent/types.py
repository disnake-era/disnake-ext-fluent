# SPDX-License-Identifier: LGPL-3.0-only

from __future__ import annotations

import datetime
from typing import Any, Callable, Union, TypeVar, Optional, TYPE_CHECKING

from babel.dates import format_time
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

if TYPE_CHECKING:
    import os
    import babel

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


class FluentTime(FluentType):
    _time: datetime.time

    def __init__(self, time_: Optional[datetime.time] = None) -> None:
        self._time = time_ or datetime.datetime.now().time()

    def format(self, locale: babel.Locale) -> str:
        return format_time(self._time)


PathT = Union[str, "os.PathLike[Any]"]
ReturnT = TypeVar("ReturnT", bound = Union[FluentType, str])
FluentFunction = Callable[..., ReturnT]
