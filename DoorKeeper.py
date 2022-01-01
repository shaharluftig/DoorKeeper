import asyncio
import secrets
import time
from datetime import datetime

import numpy as np
from imutils.video import VideoStream

import face_utils
from Config.door_keeper_config import CAPTURE_INTERVAL, OUTPUT_STRING, TEMP_IMAGE_PATH
from Config.telegram_bot_config import SHOT_PER_RECOGNIZE
from DataProviders.FSProvider import FSProvider
from Logging.PythonLogger import PythonLogger

logger = PythonLogger()


class DoorKeeper:
    def __init__(self, faces_data: list, ip_cam_url, output_stream, model="hog",
                 shots_per_recognize=SHOT_PER_RECOGNIZE):
        self.faces_data = faces_data
        self.vs = VideoStream(src=ip_cam_url).start()
        self.output_stream = output_stream
        self.model = model
        self.shots_per_recognize = shots_per_recognize

    @logger.session_log
    async def start_recognizing(self):
        while True:
            faces_matches, number_of_faces, non_empty_frame = [], 1, None
            for batch in range(self.shots_per_recognize):
                frame = self.__get_frame()
                encodings = face_utils.prepare_image(frame, model=self.model)
                if len(encodings) != 0:
                    number_of_faces, non_empty_frame = len(encodings), frame
                matches_future = [face_utils.compare_faces(self.faces_data, encoding) for encoding in encodings]
                faces_matches = filter(None, await asyncio.gather(*matches_future))
                time.sleep(CAPTURE_INTERVAL)
            matches = face_utils.determine_persons(faces_matches, number_of_faces)
            if non_empty_frame is not None:
                await self.__send_message(matches, non_empty_frame)

    def __get_frame(self):
        frame = self.vs.read()
        if frame is not None:
            return frame
        raise face_utils.VideoStreamException("Cant get frame from VideoStream")

    async def __send_message(self, matches: list, frame: np.array):
        await face_utils.save_frame_to_disk(TEMP_IMAGE_PATH, frame)
        if matches:
            persons = ",".join([str(person[0]) for person in matches])
            await self.__upload_to_output_stream(OUTPUT_STRING.format(persons=persons), TEMP_IMAGE_PATH)
        else:
            generated_name = await self.__generate_person()
            await self.__upload_to_output_stream(OUTPUT_STRING.format(persons=f"{generated_name}"),
                                                 TEMP_IMAGE_PATH)

    async def __generate_person(self, add_to_faces_data=False):
        """
        Generates a hash to unknown person, if add_to_faces_data is True,
        the unknown will be inferred (experimental!)
        """
        generated_name = f"unknown_{secrets.token_urlsafe(7)}"
        if add_to_faces_data:
            face_data = FSProvider().get_face_data(TEMP_IMAGE_PATH)
            face_data.full_name = generated_name
            self.faces_data.append(face_data)
        return generated_name

    async def __upload_to_output_stream(self, message: str, image_path: str):
        message = f"{message} timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        logger.log(message)
        asyncio.create_task(self.output_stream.notify(path=image_path, message=message))
