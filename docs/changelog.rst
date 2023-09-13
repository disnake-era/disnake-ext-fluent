.. SPDX-License-Identifier: LGPL-3.0-only

.. currentmodule:: disnake.ext.fluent

Changelog
=========

This page keeps a detailed human friendly rendering of what's new and changed
in specific versions. Please see footnote in project's README for information
about version guarantees.

.. towncrier-draft-entries:: |release| [UNRELEASED]

.. towncrier release notes start


.. _vp0p1p0:

v0.1.0
------

New Features
~~~~~~~~~~~~
- Add ``cache`` parameter to :meth:`FluentStore.l10n` to control caching at localization-level. (:issue:`1`)
- Add :attr:`FluentStore.CACHE_BY_DEFAULT` to control the default for ``cache``. (:issue:`1`)

Bug Fixes
~~~~~~~~~
- Change cache keys to include argument values in them. (:issue:`1`)
