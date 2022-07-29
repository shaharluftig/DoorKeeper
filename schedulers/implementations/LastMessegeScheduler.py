import asyncio
from datetime import datetime
from typing import List

import numpy as np

import face_utils
from config.constants import LAST_MESSAGE, TIME
from config.door_keeper_config import TEMP_IMAGE_PATH, OUTPUT_STRING, REPEATED_FACE_TIMEOUT
from output_streams.IOutputStream import IOutputStream
from schedulers.IScheduler import IScheduler


class LastMessageScheduler(IScheduler):
    def __init__(self, output_streams: List[IOutputStream], repeated_face_timeout=REPEATED_FACE_TIMEOUT):
        self.output_streams = output_streams
        self.last_message = None
        self.repeated_face_timeout = repeated_face_timeout

    async def schedule_to_output_stream(self, matches: list, frame: np.array):
        persons_in_frame = ",".join(sorted([str(person[0]) for person in matches]))
        message = OUTPUT_STRING.format(persons=persons_in_frame)
        current_time = datetime.now()
        if self.last_message is None or self.last_message[LAST_MESSAGE] != message or \
                (current_time - self.last_message[TIME]).seconds > self.repeated_face_timeout:
            self.last_message = {LAST_MESSAGE: message, TIME: current_time}
            message = self.__add_timestamp(message, current_time)
            await self.__notify_to_output_streams(message, frame)

    async def __notify_to_output_streams(self, message, frame):
        await face_utils.save_frame_to_disk(TEMP_IMAGE_PATH, frame)
        [asyncio.create_task(stream.notify(path=TEMP_IMAGE_PATH, message=message)) for stream in
         self.output_streams]

    @staticmethod
    def __add_timestamp(message: str, current_time: datetime) -> str:
        return f"{message} timestamp: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
