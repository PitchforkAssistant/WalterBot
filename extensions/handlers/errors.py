import logging
import lightbulb

plugin = lightbulb.Plugin("Error Handler")
_LOGGER = logging.getLogger(__name__)


@plugin.listener(lightbulb.SlashCommandErrorEvent)
async def memberCreate(event: lightbulb.SlashCommandErrorEvent) -> None:
    ctx = event.context
    reply = None
    match type(event.exception):
        case lightbulb.errors.NotOwner:
            reply = "You must be the owner of the bot to use this command."
        case lightbulb.errors.BotOnly:
            reply = "This command can only be used by bots."
        case lightbulb.errors.WebhookOnly:
            reply = "This command can only be used by webhooks."
        case lightbulb.errors.OnlyInGuild:
            reply = "This command can only be used in a guild."
        case lightbulb.errors.BotMissingRequiredPermission:
            reply = "I don't have the permissions required to do this."
        case lightbulb.errors.MissingRequiredRole:
            reply = "You don't have the role required to do this."
        case (lightbulb.errors.CheckFailure
              | lightbulb.errors.MissingRequiredPermission):
            reply = "You don't have the permissions required to do this."

    if reply:
        await ctx.respond(reply)
    else:
        raise event.exception


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
