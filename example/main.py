# SPDX-License-Identifier: LGPL-3.0-only

import os
import contextlib

import disnake
from disnake.ext import commands, fluent  # This library is packaged as disnake.ext.fluent


# You should typically use a custom bot class and type hint `.i18n` approritately.
class MyBot(commands.InteractionBot):
    i18n: fluent.FluentStore


# Custom functions take any number of arguments of any `Fluent*` type from
# this extension, and return single value of any `Fluent*` type.
# Read more here: https://projectfluent.org/python-fluent/fluent.runtime/stable/usage.html#custom-functions
# You can also create your own fluent types by subclassing `FluentType`.
def current_time() -> str:
    return fluent.FluentTime()


bot = MyBot(localization_provider = fluent.FluentStore(
    functions = {
        "CURRENT_TIME": current_time,  # Mapping of fluent function names to actual fluent functions
    }))

# As eveything else in Python ("unless explicitly stated otherwise"), directory path below
# is relative to where you run this from, not where this file is.
# IMPORTANT: `.load()` call must happen *before* you create any application commands. If
# you are using cogs (bad) or plugins (good), put `bot.load_extensions()` (or your custom
# extension loading logic) *after* this line.
bot.i18n.load("example/locale/")


@bot.event
async def on_ready() -> None:
    print("Ready to go!")


@bot.slash_command(  # type: ignore[reportUnknownMemberType]  # please ignore this
    description = disnake.Localized("Oops, something went wrong.", key = "example_desc"))
async def example(inter: disnake.AppCmdInter) -> None:
    await inter.response.send_message(
        # One would usually create a helper function for localizing stuff,
        # but we'll omit it here and use .`l10n()` directly.
        bot.i18n.l10n("example_text", inter.locale, { "username": str(inter.author) }) or "Sorry.")


@bot.slash_command()  # type: ignore[reportUnknownMemberType]  # please ignore this
async def another_example(inter: disnake.AppCmdInter) -> None:
    await inter.response.send_message(
        bot.i18n.l10n("another_example_text", inter.locale) or "Sorry.")


token = os.environ.get("BOT_TOKEN")

if not token:
    raise RuntimeError("You must set your bot token via BOT_TOKEN environment variable.")

with contextlib.suppress(KeyboardInterrupt):
    bot.run(token)
