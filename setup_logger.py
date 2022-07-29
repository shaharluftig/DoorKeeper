import logging
import sys

logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("logs/entrances.log", mode="w"),
    logging.StreamHandler(sys.stdout)
]
                    )
logger = logging.getLogger("DoorKeeperLogs")
