import FaceUtils
from Config.telegram_bot_config import SLEEP_INTERVAL
from Connectors.FacesDB import FacesDB
from Connectors.MongoConnector import MongoConnector
from DataProviders.FSProvider import FSProvider
from DoorKeeper import DoorKeeper
from OutputStreams.TelegramBot import TelegramBot

TELEGRAM_BOT_TOKEN = "1267323409:AAHbcf8MCqo7n34pY7D_s28T_dxvHmiINpE"
TELEGRAM_BOT_CHAT_ID = "713846533"

IP_CAMERA_URL = "http://192.168.1.12:8080/video"

INFER_PROVIDERS = True
PROVIDERS = [FSProvider("./Images")]


def infer_providers(providers):
    user_faces = []
    for provider in providers:
        user_faces += provider.get_faces_data()
    return user_faces


if __name__ == '__main__':
    db = FacesDB(*FaceUtils.get_mongo_connection_param())
    if INFER_PROVIDERS:
        data = infer_providers(PROVIDERS)
        db.add_complex_object(data, many=True)

    faces_data = db.collect_all_data()
    output_stream = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_CHAT_ID, SLEEP_INTERVAL)
    DoorKeeper(IP_CAMERA_URL, output_stream).start_recognizing(faces_data)
