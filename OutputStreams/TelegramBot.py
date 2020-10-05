import time

import telegram

from OutputStreams.IOutputStream import IOutputStream


class TelegramBot(IOutputStream):

    def __init__(self, bot_token: str, bot_chat_id: str, sleep_interval: int):
        self.bot_chat_id = bot_chat_id
        self.bot = telegram.Bot(token=bot_token)
        self.sleep_interval = sleep_interval

    def send_message(self, message: str):
        self.bot.send_message(self.bot_chat_id, message)
        time.sleep(self.sleep_interval)

    def send_image(self, path: str, caption=None):
        self.bot.send_photo(self.bot_chat_id, photo=open(path, 'rb'), caption=caption)
        time.sleep(self.sleep_interval)
