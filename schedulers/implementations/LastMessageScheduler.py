import asyncio
from datetime import datetime
from typing import List

import numpy as np

import face_utils
from config.door_keeper_config import TEMP_IMAGE_PATH, REPEATED_FACE_TIMEOUT
from models.Guests import Guests
from output_streams.IOutputStream import IOutputStream
from schedulers.Scheduler import Scheduler


class LastMessageScheduler(Scheduler):
    def __init__(self, output_streams: List[IOutputStream], repeated_face_timeout=REPEATED_FACE_TIMEOUT):
        super().__init__(output_streams)
        self.last_guests: Guests = None
        self.repeated_face_timeout = repeated_face_timeout

    async def schedule_to_output_stream(self, matches: list, frame: np.array):
        names_in_frame = sorted([str(person[0]) for person in matches])
        current_guests = Guests(names=names_in_frame, timestamp=datetime.now())
        if self.last_guests is None or self.last_guests.names != current_guests.names or \
                (current_guests.timestamp - self.last_guests.timestamp).seconds > self.repeated_face_timeout:
            self.last_guests = current_guests
            await self.__notify_to_output_streams(current_guests, frame)

    async def __notify_to_output_streams(self, door_message: Guests, frame: np.array):
        await face_utils.save_frame_to_disk(TEMP_IMAGE_PATH, frame)
        [asyncio.create_task(stream.notify(path=TEMP_IMAGE_PATH, guests=door_message)) for stream in
         self.output_streams]
