# SPDX-License-Identifier: LGPL-3.0-only

from pathlib import Path

from fluent.runtime.types import fluent_date, fluent_number

from .types import PathT

__all__ = ("fluent_date", "fluent_number")


def search_ftl_files(path: PathT) -> list[str]:
    """Search for FTL files in the provided directory.

    Parameters
    ----------
    path: Union[:class:`str`, :class:`os.PathLike`]
        The path to search for FTL files.

    Returns
    -------
    list[:class:`os.PathLike`]
        A list of paths to FTL files.
    """
    path = Path(path)

    if not path.is_dir():
        raise RuntimeError(f"Path '{path}' does not exist or is not a directory.")

    return [str(Path(*(file.parts[2:]))) for file in path.glob("**/*.ftl")]


def search_languages(path: PathT) -> list[Path]:
    """Search for languages in the provided directory.

    Parameters
    ----------
    path: Union[:class:`str`, :class:`os.PathLike`]
        The path to search for languages.

    Returns
    -------
    list[str]
        A list of languages.
    """
    path = Path(path)

    if not path.is_dir():
        raise RuntimeError(f"Path '{path}' does not exist or is not a directory.")

    return [Path(*dir_.parts[1:]) for dir_ in path.iterdir() if dir_.is_dir()]
