from Config.telegram_bot_config import SLEEP_INTERVAL
from Connectors.FacesDB import FacesDB
from DataProviders.FSProvider import FSProvider
from DoorKeeper import DoorKeeper
from OutputStreams.TelegramBot import TelegramBot

MONGO_PORT = 27017
MONGO_HOST = "localhost"
MONGO_COLLECTION = "faces"
MONGO_DB = "facesdb"

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_BOT_CHAT_ID = ""

IP_CAMERA_URL = ""

INFER_PROVIDERS = True
PROVIDERS = [FSProvider("./Images")]


def infer_providers(providers):
    user_faces = []
    for provider in providers:
        user_faces += provider.get_faces_data()
    return user_faces


if __name__ == '__main__':
    db = FacesDB(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION)
    if INFER_PROVIDERS:
        data = infer_providers(PROVIDERS)
        db.add_complex_object(data, many=True)

    faces_data = db.collect_all_data()
    output_stream = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_CHAT_ID, SLEEP_INTERVAL)
    DoorKeeper(IP_CAMERA_URL, output_stream).start_recognizing(faces_data)
