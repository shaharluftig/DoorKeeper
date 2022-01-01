import asyncio

import telegram

from OutputStreams.IOutputStream import IOutputStream


class TelegramBot(IOutputStream):

    def __init__(self, bot_token: str, bot_chat_id: str):
        self.bot_chat_id = bot_chat_id
        self.bot = telegram.Bot(token=bot_token)

    async def __send_message(self, message: str):
        self.bot.send_message(self.bot_chat_id, message)

    async def __send_image(self, path: str, caption=None):
        self.bot.send_photo(self.bot_chat_id, photo=open(path, 'rb'), caption=caption)

    async def notify(self, path: str, message):
        await self.__send_image(path, message)
        await asyncio.sleep(3)
