import time

import numpy as np
from imutils.video import VideoStream

import FaceUtils
from Config import CAPTURE_INTERVAL, TEMP_IMAGE_PATH, OUTPUT_STRING
from Config.telegram_bot_config import SHOT_PER_RECOGNIZE
from Logging.PythonLogger import PythonLogger

logger = PythonLogger()


class DoorKeeper:
    def __init__(self, ip_cam_url: str, output_stream, model="hog", shots_per_recognize=SHOT_PER_RECOGNIZE):
        self.vs = VideoStream(src=ip_cam_url).start()
        self.output_stream = output_stream
        self.model = model
        self.shots_per_recognize = shots_per_recognize

    @logger.session_log
    def start_recognizing(self, faces_data: dict):
        while True:
            faces_matches, number_of_faces, non_empty_frame = [], 1, None
            for batch in range(self.shots_per_recognize):
                frame = self.__get_frame()
                encodings = FaceUtils.get_frame_encoding(frame, model=self.model)
                if len(encodings) != 0:
                    number_of_faces, non_empty_frame = len(encodings), frame
                for encoding in encodings:
                    match = FaceUtils.compare_faces(faces_data, encoding)
                    if match: faces_matches.append(match)
                    time.sleep(CAPTURE_INTERVAL)
            matches = FaceUtils.determine_persons(faces_matches, number_of_faces)
            if non_empty_frame is not None:
                self.__send_message(matches, non_empty_frame)

    def __get_frame(self):
        frame = self.vs.read()
        if frame is not None:
            return frame
        raise FaceUtils.FaceException("Cant get frame from VideoStream")

    def __send_message(self, matches: list, frame: np.array):
        FaceUtils.save_frame_to_disk(TEMP_IMAGE_PATH, frame)
        if matches:
            persons = ','.join([person[0] for person in matches])
            self.__upload_to_output_stream(OUTPUT_STRING.format(persons=persons), TEMP_IMAGE_PATH)
        else:
            self.__upload_to_output_stream(OUTPUT_STRING.format(persons="Unknown"), TEMP_IMAGE_PATH)

    def __upload_to_output_stream(self, message: str, image_path: str):
        logger.log(message)
        self.output_stream.send_image(path=image_path, caption=message)
