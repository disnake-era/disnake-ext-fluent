# SPDX-License-Identifier: LGPL-3.0-only

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Callable, TypeVar, Union

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
    from typing_extensions import Self

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
    "FluentTime",
    "FluentType",
)


def FluentBool(value: bool) -> str:  # noqa: N802, FBT001
    """Transform boolean value to lowercase string."""
    return str(value).lower()


class FluentTime(FluentType):
    _time: datetime.time

    def __init__(self: Self, time_: datetime.time | None = None) -> None:
        self._time = time_ or datetime.datetime.now(tz = datetime.timezone.utc).time()

    def format(self: Self, locale: babel.Locale) -> str:  # noqa: A003, ARG002
        return format_time(self._time)


PathT = Union[str, "os.PathLike[Any]"]
ReturnT = TypeVar("ReturnT", bound = Union[FluentType, str])
FluentFunction = Callable[..., ReturnT]
