from DataProviders.FSProvider import FSProvider

# Env Setup
TELEGRAM_BOT_TOKEN = "1267323409:AAHbcf8MCqo7n34pY7D_s28T_dxvHmiINpE"
TELEGRAM_BOT_CHAT_ID = "713846533"

IP_CAMERA_URL = "http://192.168.1.12:8080/video"
INFER_PROVIDERS = True
PROVIDERS = [FSProvider("./Images")]