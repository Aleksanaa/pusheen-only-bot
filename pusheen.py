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
        self.group_id = f"-{getenv('BOT_GROUP')}"
        self.config = getenv("BOT_CONFIG")
        with open(self.config, mode="w+") as c:
            self.stickers = c.read().split("\n")

        self.updater.dispatcher.add_handler(
            MessageHandler(filters.Filters.all, self.intercept)
        )

        self.updater.start_polling()

    def sync_config(self):
        self.stickers = [*set(self.stickers)]
        with open(self.config, mode="w") as c:
            c.write("\n".join(self.stickers))
            c.close()

    def intercept(self, update: Update, context: CallbackContext):
        message = update.message
        if (
            message.from_user
            in [admin.user for admin in message.chat.get_administrators()]
            and message.text
        ):
            if message.text.startswith("add"):
                self.stickers.append(message.text.split()[1])
            elif message.text.startswith("del"):
                self.stickers.remove(message.text.split()[1])
            elif message.text.startswith("list"):
                message.reply_text(
                    "The available stickers:\n" + "\n".join(self.stickers)
                )
            self.sync_config()

        if not (message.sticker and message.sticker.set_name in self.stickers):
            message.delete()


if __name__ == "__main__":
    pusheen = Pusheen()
