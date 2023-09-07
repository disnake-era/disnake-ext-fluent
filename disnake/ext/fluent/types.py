# SPDX-License-Identifier: LGPL-3.0-only

import os
from typing import Any, Union


__all__ = ("PathT",)


PathT = Union[str, os.PathLike[Any]]
