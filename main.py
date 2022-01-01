import asyncio

from Config import config
from Connectors.FacesDB import FacesDB
from DoorKeeper import DoorKeeper
from OutputStreams.TelegramBot import TelegramBot
from face_utils import infer_providers


async def main():
    db = FacesDB(host=config.mongo_host, port=int(config.mongo_port), username=config.mongo_username,
                 password=config.mongo_password, db=config.mongo_db, collection=config.mongo_collection)

    if config.infer_providers:
        infer_providers(config.providers, db)

    faces_data = db.collect_all_data()
    telegram_bot = TelegramBot(config.telegram_bot_token, config.telegram_bot_chat_id)
    await DoorKeeper(faces_data, ip_cam_url=config.ip_camera_url, output_stream=telegram_bot).start_recognizing()


if __name__ == '__main__':
    asyncio.run(main())
