import os

from DataProviders.FSProvider import FSProvider

# Env Setup
ENV = "prod"


class DefaultConfig:
    telegram_bot_token = ""
    telegram_bot_chat_id = ""
    mongo_collection = "facedb"

    infer_providers = True
    providers = [FSProvider("./Images")]


class ProdConfig(DefaultConfig):
    ip_camera_url = ""
    mongo_username = os.environ.get('MONGODB_USERNAME')
    mongo_password = os.environ.get('MONGODB_PASSWORD')
    mongo_host = os.environ.get('MONGODB_HOSTNAME')
    mongo_port = int(os.environ.get('MONGODB_PORT'))
    mongo_db = os.environ.get('MONGODB_DATABASE')


class DevConfig(DefaultConfig):
    ip_camera_url = 0
    mongo_username = "admin"
    mongo_password = "admin"
    mongo_host = "localhost"
    mongo_port = 27017
    mongo_db = "facedb"


config = ProdConfig if ENV == "prod" else DevConfig
