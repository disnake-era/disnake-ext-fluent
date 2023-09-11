# SPDX-License-Identifier: LGPL-3.0-only

from pathlib import Path
from typing import List

from .types import PathT

from fluent.runtime.types import fluent_date, fluent_number

__all__ = ("fluent_date", "fluent_number")


def search_ftl_files(path: PathT) -> List[str]:
    """Search for FTL files in the provided directory.

    Parameters
    ----------
    path: Union[:class:`str`, :class:`os.PathLike`]
        The path to search for FTL files.

    Returns
    -------
    List[:class:`os.PathLike`]
        A list of paths to FTL files.
    """
    path = Path(path)

    if not path.is_dir():
        raise RuntimeError(f"Path '{path}' does not exist or is not a directory.")

    return [file.parts[-1] for file in path.glob("**/*.ftl")]


def search_languages(path: PathT) -> List[str]:
    """Search for languages in the provided directory.

    Parameters
    ----------
    path: Union[:class:`str`, :class:`os.PathLike`]
        The path to search for languages.

    Returns
    -------
    List[:class:`str`]
        A list of languages.
    """
    path = Path(path)

    if not path.is_dir():
        raise RuntimeError(f"Path '{path}' does not exist or is not a directory.")

    return [dir.parts[-1] for dir in path.iterdir() if dir.is_dir()]
