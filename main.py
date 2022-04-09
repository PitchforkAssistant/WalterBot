import lightbulb

from config import Config


def start_bot() -> None:
    config = Config()
    bot = lightbulb.BotApp(
        token=config.token
    )
    bot.load_extensions_from("./extensions", recursive=True)
    bot.run()


if __name__ == "__main__":
    start_bot()
