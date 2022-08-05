import asyncio

from DoorKeeper import DoorKeeper
from config import config, ENV
from connectors.implementations.FacesDB import FacesDB
from face_utils import infer_providers
from output_streams.implementations.TelegramBot import TelegramBot
from schedulers.implementations.LastMessageScheduler import LastMessageScheduler
from setup_logger import logger


async def main():
    logger.info(f"Running on {ENV} configuration")
    db = FacesDB(host=config.mongo_host, port=int(config.mongo_port), username=config.mongo_username,
                 password=config.mongo_password, db=config.mongo_db, collection=config.mongo_collection)

    if config.infer_providers:
        infer_providers(config.providers, db)

    faces_data = db.collect_all_data()
    telegram_bot = TelegramBot(config.telegram_bot_token, config.telegram_bot_chat_id)
    await DoorKeeper(faces_data, ip_cam_url=config.ip_camera_url,
                     scheduler=LastMessageScheduler([telegram_bot])).start_recognizing()


if __name__ == '__main__':
    asyncio.run(main())
