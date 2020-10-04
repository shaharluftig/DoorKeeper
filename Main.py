from Config.telegram_bot_config import SLEEP_INTERVAL
from Connectors.FacesDB import FacesDB
from DoorKeeper import DoorKeeper
from OutputStreams.TelegramBot import TelegramBot

REDIS_DB = 0
REDIS_PORT = ""
REDIS_HOST = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_BOT_CHAT_ID = ""
IP_CAMERA_URL = ""
INFER_IMAGE_FOLDER = True

if __name__ == '__main__':
    db = FacesDB(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    if INFER_IMAGE_FOLDER:
        db.infer_image_folder("./Images")
    data = db.collect_all_data()
    output_stream = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_CHAT_ID, SLEEP_INTERVAL)
    DoorKeeper(IP_CAMERA_URL, output_stream).start_recognizing(data)
