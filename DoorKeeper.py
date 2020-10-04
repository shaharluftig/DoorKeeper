import time

from imutils.video import VideoStream

import FaceUtils
from Config import CAPTURE_INTERVAL, OUTPUT_STRING
from Logging.PythonLogger import PythonLogger

logger = PythonLogger()


class DoorKeeper:
    def __init__(self, ip_cam_url, output_stream, model="hog", shots_per_recognize=3):
        self.vs = VideoStream(src=ip_cam_url).start()
        self.output_stream = output_stream
        self.model = model
        self.shots_per_recognize = shots_per_recognize

    @logger.session_log
    def start_recognizing(self, faces_data):
        while True:
            faces_matches, number_of_faces = [], 1
            for batch in range(self.shots_per_recognize):
                encodings = FaceUtils.get_frame_encoding(frame=self.vs.read(), model=self.model)
                number_of_faces = len(encodings) if len(encodings) != 0 else number_of_faces
                for encoding in encodings:
                    match = FaceUtils.compare_faces(faces_data, encoding)
                    if match: faces_matches.append(match)
                    time.sleep(CAPTURE_INTERVAL)
            matches = FaceUtils.determine_persons(faces_matches, number_of_faces)
            self.__send_message(matches)

    def __send_message(self, matches):
        if matches:
            persons = [person[0] for person in matches]
            door_msg = OUTPUT_STRING.format(persons=persons)
            logger.log(door_msg)
            self.output_stream.send_message(door_msg)
