import hikari
import lightbulb
import configparser


def start_bot() -> None:
    config = configparser.ConfigParser()
    config.read("configs/config.ini")
    bot = lightbulb.BotApp(
        token=config["DEFAULT"]["token"],
        intents=hikari.Intents.ALL
    )
    bot.load_extensions_from("./extensions", recursive=True)
    bot.run()


if __name__ == "__main__":
    start_bot()
