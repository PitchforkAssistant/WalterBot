import hikari
import lightbulb
import configparser

plugin = lightbulb.Plugin("Welcome")
config = configparser.ConfigParser()
config["DEFAULT"] = {"enabled": "no"}
config.read("configs/welcome.ini")


def set_config_guild_value(guild: str, option: str, value: str) -> None:
    if guild not in config:
        config[guild] = {}
    config[guild][option] = value
    with open("configs/welcome.ini", "w") as configfile:
        config.write(configfile)


@plugin.listener(hikari.events.MemberCreateEvent)
async def memberCreate(event: hikari.events.MemberCreateEvent) -> None:
    pass


@plugin.command()
@lightbulb.add_checks(
    lightbulb.checks.has_role_permissions(
        hikari.Permissions.MANAGE_GUILD))
@lightbulb.add_checks(lightbulb.checks.guild_only)
@lightbulb.option(
    "channel",
    "Channel you wish to set as the welcome channel.",
    hikari.OptionType.CHANNEL,
    channel_types=[hikari.ChannelType.GUILD_TEXT],
    required=True)
@lightbulb.command("setwelcomechannel", "Unload specified extension.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def set_welcome_channel(ctx: lightbulb.context.Context) -> None:
    assert ctx.guild_id is not None  # Should never fail because of guild_only
    set_config_guild_value(str(ctx.guild_id),
                           "channel",
                           str(ctx.options.channel.id))
    await ctx.respond(f"Set welcome channel to <#{ctx.options.channel.id}>.")


@plugin.command()
@lightbulb.add_checks(
    lightbulb.checks.has_role_permissions(
        hikari.Permissions.MANAGE_GUILD))
@lightbulb.add_checks(lightbulb.checks.guild_only)
@lightbulb.option(
    "enabled",
    "Enable the welcome feature.",
    required=True,
    choices=[
        hikari.CommandChoice(name="on", value="on"),
        hikari.CommandChoice(name="off", value="off")])
@lightbulb.command("setwelcomeenabled", "Unload specified extension.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def set_welcome_enabled(ctx: lightbulb.context.Context) -> None:
    assert ctx.guild_id is not None  # Should never fail because of guild_only
    set_config_guild_value(str(ctx.guild_id), "enabled", ctx.options.enabled)
    if str(ctx.guild_id) in config and "channel" in config[str(ctx.guild_id)]:
        await ctx.respond(f"Welcome feature is now {ctx.options.enabled}.")
    else:
        await ctx.respond(
            f"Welcome feature is now {ctx.options.enabled},"
            + " you have not set a welcome channel yet.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
