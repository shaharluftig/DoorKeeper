import asyncio
from typing import List

from imutils.video import VideoStream

import face_utils
from encoders.implementations.FaceEncoder import FaceEncoder
from face_compares.implementations.FaceDistanceCompare import FaceDistanceCompare
from models.UserFace import UserFace
from output_streams.IOutputStream import IOutputStream
from schedulers.implementations.LastMessegeScheduler import LastMessageScheduler
from setup_logger import logger


class DoorKeeper:
    def __init__(self, faces_data: List[UserFace], ip_cam_url: str, output_streams: List[IOutputStream],
                 model: str = "hog"):
        self.faces_data = faces_data
        self.vs = VideoStream(src=ip_cam_url).start()
        self.scheduler = LastMessageScheduler(output_streams)
        self.model = model
        self.last_message = None
        self.encoder = FaceEncoder()
        self.face_compare = FaceDistanceCompare()

    async def start_recognizing(self):
        logger.info("Start recognizing")
        while True:
            number_of_faces, non_empty_frame = 1, None
            frame = self.__get_frame()
            encodings = self.encoder.encode(frame)
            if len(encodings) != 0:
                number_of_faces, non_empty_frame = len(encodings), frame
            matches_future = [self.face_compare.compare_faces(self.faces_data, encoding) for encoding in encodings]
            faces_matches = list(filter(None, await asyncio.gather(*matches_future)))
            matches = face_utils.determine_persons(faces_matches, number_of_faces)
            if non_empty_frame is not None:
                await self.scheduler.schedule_to_output_stream(matches, non_empty_frame)

    def __get_frame(self):
        frame = self.vs.read()
        if frame is not None:
            return frame
        raise face_utils.VideoStreamException("Cant get frame from VideoStream")
