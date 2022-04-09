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
@lightbulb.command("reload", "Reloads specified extension.")
@lightbulb.implements(commands.SlashCommand)
async def reload(ctx: lightbulb.context.Context) -> None:

    # Find module to reload.
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

    _LOGGER.info(f"Attempting to reload {target_module}...")
    try:
        _BOT.reload_extensions(target_module)
    except Exception as e:
        _LOGGER.exception(e)
        await ctx.respond("Something went wrong!")
    else:
        _LOGGER.info(f"Reloaded {target_module}.")
        await ctx.respond(f"Reloaded {ctx.options.extension}.")


def load(bot: lightbulb.BotApp) -> None:
    global _BOT
    _BOT = bot
    bot.command(reload)


def unload(bot: lightbulb.BotApp) -> None:
    if command := bot.get_slash_command("reload"):
        bot.remove_command(command)
