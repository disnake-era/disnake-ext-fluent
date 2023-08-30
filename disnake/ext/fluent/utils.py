# SPDX-License-Identifier: LGPL-3.0-only

from pathlib import Path

from .types import PathT


def search_ftl_files(path: PathT) -> list[str]:
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

    return [str(file) for file in path.glob("**/*.ftl")]


def search_languages(path: PathT) -> list[str]:
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

    return [str(dir) for dir in path.iterdir() if dir.is_dir()]
