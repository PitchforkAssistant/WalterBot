import lightbulb
from lightbulb import commands


@lightbulb.option("text", "Any text.")
@lightbulb.command("echo", "Repeats anything you write.")
@lightbulb.implements(commands.SlashCommand)
async def echo(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(ctx.options.text)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(echo)


def unload(bot: lightbulb.BotApp) -> None:
    if command := bot.get_slash_command("echo"):
        bot.remove_command(command)
