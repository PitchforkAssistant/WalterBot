import logging
import lightbulb
from lightbulb import checks
from lightbulb import commands
from lightbulb.errors import ExtensionNotFound

_BOT: lightbulb.BotApp
_LOGGER = logging.getLogger(__name__)


@lightbulb.add_checks(checks.owner_only)
@lightbulb.option("extension", "One of the bot's unloaded extensions.")
@lightbulb.command("load", "Loads specified extension.")
@lightbulb.implements(commands.SlashCommand)
async def load_cmd(ctx: lightbulb.context.Context) -> None:
    target_module = ctx.options.extension
    if not target_module.startswith("extensions."):
        target_module = "extensions." + target_module

    _LOGGER.info(f"Attempting to load {target_module}...")
    try:
        _BOT.load_extensions(target_module)
    except ExtensionNotFound:
        await ctx.respond(f"Extension {target_module} not found.")
    except Exception as e:
        _LOGGER.exception(e)
        await ctx.respond("Something went wrong!")
    else:
        _LOGGER.info(f"Loaded {target_module}.")
        await ctx.respond(f"Loaded {ctx.options.extension}.")


def load(bot: lightbulb.BotApp) -> None:
    global _BOT
    _BOT = bot
    bot.command(load_cmd)


def unload(bot: lightbulb.BotApp) -> None:
    if command := bot.get_slash_command("load"):
        bot.remove_command(command)
