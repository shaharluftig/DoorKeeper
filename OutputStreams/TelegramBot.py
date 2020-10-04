import time

import requests

from OutputStreams.IOutputStream import IOutputStream


class TelegramBot(IOutputStream):

    def __init__(self, bot_token, bot_chat_id, sleep_interval):
        self.sleep_interval = sleep_interval
        self.bot_chat_id = bot_chat_id
        self.bot_token = bot_token
        self.session = requests.Session()

    def send_message(self, message):
        msg = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + \
              self.bot_chat_id + '&parse_mode=Markdown&text=' + message
        self.session.get(msg)
        time.sleep(self.sleep_interval)
