import sys
import hikari
import logging
import lightbulb
from lightbulb import checks
from lightbulb import commands

_BOT: lightbulb.BotApp
_LOGGER = logging.getLogger(__name__)


@lightbulb.add_checks(
    checks.has_role_permissions(
        hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("extension", "One of the bot's extensions.")
@lightbulb.command("unload", "Unload specified extension.")
@lightbulb.implements(commands.SlashCommand)
async def unload_ext(ctx: lightbulb.context.Context) -> None:

    # Find module to unload.
    target_module = None
    for module in sys.modules:
        if not module.startswith("extensions."):
            continue
        if (module.endswith(f".{ctx.options.extension}")
                or module == ctx.options.extension):
            target_module = module
            break

    if target_module is None:
        await ctx.respond(f"No such loaded extension: {ctx.options.extension}")
        return

    _LOGGER.info(f"Attempting to unload {target_module}...")
    try:
        _BOT.unload_extensions(target_module)
    except Exception as e:
        _LOGGER.exception(e)
        await ctx.respond("Something went wrong!")
    else:
        _LOGGER.info(f"Unloaded {target_module}.")
        await ctx.respond(f"Unloaded {ctx.options.extension}.")


def load(bot: lightbulb.BotApp) -> None:
    global _BOT
    _BOT = bot
    bot.command(unload_ext)


def unload(bot: lightbulb.BotApp) -> None:
    if command := bot.get_slash_command("unload"):
        bot.remove_command(command)
