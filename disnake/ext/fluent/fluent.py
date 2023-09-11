# SPDX-License-Identifier: LGPL-3.0-only

import logging
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Self

from disnake import Locale
from disnake import LocalizationProtocol, LocalizationWarning, LocalizationKeyError
from fluent.runtime import FluentResourceLoader, FluentLocalization as FluentLocalizator

from .types import FluentFunction, PathT, ReturnT
from .utils import search_ftl_files, search_languages

__all__ = ("FluentStore", )
logger = logging.getLogger(__name__)


class FluentStore(LocalizationProtocol):
    """:class:`disnake.LocalizationProtocol` implementation for Fluent.

    Parameters
    ----------
    strict: :class:`bool`
        If ``True``, the store will raise :exc:`disnake.LocalizationKeyError` if a key or
        locale is not found.
    default_language: :class:`str`
        The "fallback" language to use if localization for the desired languages is not found.
        Defaults to ``"en-US"``.

    .. versionadded:: 0.1.0
    """

    _strict: bool
    _default_language: str
    _langs: List[str]
    _loader: Optional[FluentResourceLoader]
    _localizators: Dict[str, FluentLocalizator]
    _localization_cache: Dict[str, str]
    _disnake_localization_cache: Dict[str, Dict[str, str]]
    _functions: Optional[Dict[str, FluentFunction[Any]]]

    def __init__(
        self: Self,
        *,
        strict: bool = False,
        default_language: str = "en-US",
        functions: Optional[Dict[str, FluentFunction[ReturnT]]] = None,
    ) -> None:
        self._strict = strict
        self._default_language = default_language
        self._functions = functions

        self._loader = None
        self._localizators = {}
        self._localization_cache = {}
        self._disnake_localization_cache = {}

        logger.info("FluentStore initialized.")

    def get(self: Self, key: str) -> Optional[Dict[str, str]]:
        """Localization retriever for disnake. You should use :meth:`.l10n` instead.

        Parameters
        ----------
        key: :class:`str`
            The lookup key.

        Raises
        ------
        LocalizationKeyError
            No localizations for the provided key were found.

        Returns
        -------
        Optional[Dict[:class:`str`, :class:`str`]]
            The localizations for the provided key.
            Returns ``None`` if no localizations could be found.
        """
        if not self._loader:
            raise RuntimeError("FluentStore was not initialized yet.")

        logger.debug(f"disnake requested localizations for key {key}")

        localizations = self._disnake_localization_cache.get(key)

        if not localizations:
            logger.debug(f"disnake cache miss for key {key}")

            localizations = {}

            for lang in self._langs:
                localizations[lang] = self.l10n(key, lang)

            self._disnake_localization_cache[key] = localizations

        return localizations

    def load(self: Self, path: PathT) -> None:
        """Initialize all internal attributes.

        `path` must point to a directory structured as per Fluent's guidelines.

        Parameters
        ----------
        path: Union[:class:`str`, :class:`os.PathLike`]
            The path to the Fluent localization directory to load.

        Raises
        ------
        RuntimeError
            The provided path is invalid or couldn't be loaded
        """
        path = Path(path)

        if not path.is_dir():
            raise RuntimeError(f"Path '{path}' does not exist or is not a directory.")

        self._langs = search_languages(path)
        resources = search_ftl_files(path)

        logger.info("Setting up FluentStore.")
        logger.debug(
            f"Constructing localizators for locales {self._langs} using resource {resources}.")

        self._loader = FluentResourceLoader(str(path) + "/{locale}")

        for lang in self._langs:
            self._localizators[lang] = FluentLocalizator(
                [lang, self._default_language],
                resources,
                self._loader,
                functions = self._functions,
            )

    def l10n(
        self: Self,
        key: str,
        locale: Union[Locale, str],
        values: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        if not self._loader:
            raise RuntimeError("FluentStore was not initialized yet.")

        logger.debug(f"Localization requested for key {key} and locale {locale!s}.")

        if cached := self._localization_cache.get(key + ":" + str(locale)):
            return cached

        logger.debug(f"Regular cache miss for key {key} and locale {locale!s}.")

        localizator = self._localizators.get(str(locale))

        if not localizator:
            warnings.warn(f"Localizator not found for locale {locale!s}.", LocalizationWarning)
            return None

        values = values or {}

        localized = localizator.format_value(key, values)

        if localized != key:  # translation *was* found
            self._localization_cache[key + ":" + str(locale)] = localized
            return localized

        # translation was *not* found

        if self._strict:
            raise LocalizationKeyError(f"Key {key} not found for locale {locale!s}.")

        warnings.warn(f"Key {key} not found for locale {locale!s}.", LocalizationWarning)

        return None

    def reload(self: Self) -> None:
        """Clear localizations and reload all previously loaded FTLs again.

        If an exception occurs, the previous data gets restored and the exception is re-raised.
        See :func:`.load` for possible raised exceptions.

        Not implemented yet.
        """
        raise NotImplementedError
