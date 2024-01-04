# SPDX-License-Identifier: LGPL-3.0-only

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from typing_extensions import Self

from disnake import Locale, LocalizationKeyError, LocalizationProtocol, LocalizationWarning
from fluent.runtime import FluentLocalization as FluentLocalizator
from fluent.runtime import FluentResourceLoader

from .utils import search_ftl_files, search_languages

if TYPE_CHECKING:
    from .types import FluentFunction, PathT, ReturnT

__all__ = ("FluentStore", )
logger = logging.getLogger(__name__)


class FluentStore(LocalizationProtocol):
    """:class:`disnake.LocalizationProtocol` implementation for Fluent.

    Attributes
    ----------
    CACHE_BY_DEFAULT: ClassVar[:class:`str`]
        Controls the default value for ``cache`` in :meth:`.l10n`.
        Does not affect caching of static-by-definition keys like
        application commands' names/descriptions.
        Defaults to ``False``.

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

    CACHE_BY_DEFAULT: ClassVar[bool] = False

    _strict: bool
    _default_language: str
    _langs: list[str]
    _loader: FluentResourceLoader | None
    _localizators: dict[str, FluentLocalizator]
    _localization_cache: dict[str, str]
    _disnake_localization_cache: dict[str, dict[str, str]]
    _functions: dict[str, FluentFunction[Any]] | None

    def __init__(
        self: Self,
        *,
        strict: bool = False,
        default_language: str = "en-US",
        functions: dict[str, FluentFunction[ReturnT]] | None = None,
    ) -> None:
        self._strict = strict
        self._default_language = default_language
        self._functions = functions

        self._loader = None
        self._localizators = {}
        self._localization_cache = {}
        self._disnake_localization_cache = {}

        logger.info("FluentStore initialized.")

    def get(self: Self, key: str) -> dict[str, str] | None:
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

        logger.debug("disnake requested localizations for key %s", key)

        localizations = self._disnake_localization_cache.get(key)

        if not localizations:
            logger.debug("disnake cache miss for key %s", key)

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
            "Constructing localizators for locales %s using resource %s.",
            self._langs,
            resources,
        )

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
        locale: Locale | str,
        values: dict[str, Any] | None = None,
        *,
        cache: bool | None = None,
    ) -> str | None:
        if not self._loader:
            raise RuntimeError("FluentStore was not initialized yet.")

        logger.debug("Localization requested for key %s and locale %s.", key, locale)

        cache = cache or FluentStore.CACHE_BY_DEFAULT
        cache_key = key + ":" + str(locale) + ":" + str(values)

        if cache:
            if cached := self._localization_cache.get(cache_key):
                return cached

            logger.debug("Regular cache miss for key %s and locale %s.", key, locale)

        localizator = self._localizators.get(str(locale))

        if not localizator:
            warnings.warn(f"Localizator not found for locale {locale!s}.", LocalizationWarning)
            return None

        values = values or {}

        localized = localizator.format_value(key, values)

        if localized != key:  # translation *was* found
            if cache:
                self._localization_cache[cache_key] = localized
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
