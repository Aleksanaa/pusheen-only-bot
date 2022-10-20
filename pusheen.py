# This only works on python-telegram-bot 13.* but not on 20.*

from telegram.ext import (
    Updater,
    MessageHandler,
    filters,
    CallbackContext,
)
from telegram import Update
from os import getenv


class Pusheen:
    def __init__(self) -> None:
        self.updater = Updater(getenv("BOT_TOKEN"))
        self.config = getenv("BOT_CONFIG")
        try:
            with open(self.config, mode="r") as c:
                self.stickers = c.read().split("\n")
                c.close()
        except FileNotFoundError:
            self.stickers = []

        self.updater.dispatcher.add_handler(
            MessageHandler(filters.Filters.all, self.intercept)
        )

        self.updater.start_polling()

    def sync_config(self):
        with open(self.config, mode="w") as c:
            c.write("\n".join(self.stickers))
            c.close()

    def intercept(self, update: Update, context: CallbackContext):
        message = update.message
        if message.text and message.from_user in [
            admin.user for admin in message.chat.get_administrators()
        ]:
            if message.text == ("?"):
                message.reply_markdown_v2(
                    "The available stickers:\n\n"
                    + "\n".join(
                        [
                            f"[{sticker}](t.me/addstickers/{sticker})"
                            for sticker in self.stickers
                        ]
                    )
                )
            else:
                for op in message.text.split():
                    if op.startswith("+") and op.lstrip("+") not in self.stickers:
                        self.stickers.append(op.lstrip("+"))
                    elif op.startswith("-") and op.lstrip("-") in self.stickers:
                        self.stickers.remove(op.lstrip("-"))
                self.sync_config()

        if not (message.sticker and message.sticker.set_name in self.stickers):
            message.delete()


if __name__ == "__main__":
    pusheen = Pusheen()
