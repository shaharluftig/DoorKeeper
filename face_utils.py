import urllib.request
from collections import Counter

import cv2
import face_recognition
import imutils
import numpy as np

from Config.door_keeper_config import THRESHOLD
from Logging.PythonLogger import PythonLogger

logger = PythonLogger()


class VideoStreamException(Exception):
    """Raised when VideoStream is unreachable """
    pass


def show_image(image):
    cv2.imshow("face", image)
    cv2.waitKey(0)


def prepare_image(image, model="hog") -> np.array:
    rgb = imutils.resize(image, width=750)
    boxes = face_recognition.face_locations(rgb, model=model)
    encoding = face_recognition.face_encodings(rgb, boxes)
    return encoding


def determine_persons(matches: list, number_of_faces: int):
    return Counter(matches).most_common(number_of_faces)


async def compare_faces(faces_data: list, encoding: np.array):
    distances = [1 - distance for distance in
                 face_recognition.face_distance([person.encoding for person in faces_data], encoding)]
    faces_data_distances = dict(zip(distances, faces_data))
    best_match = max(faces_data_distances, key=float)
    if best_match >= THRESHOLD:
        return faces_data_distances[best_match]


async def save_frame_to_disk(file_name: str, frame: np.array):
    if frame is not None:
        cv2.imwrite(file_name, frame)


def infer_url_image(url: str, model="hog") -> np.array:
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return prepare_image(cv2.imdecode(image, cv2.COLOR_BGR2RGB), model)


def infer_fs_image(path: str, model="hog") -> np.array:
    logger.log(f"Inferring {path}")
    return prepare_image(cv2.imread(path, cv2.COLOR_BGR2RGB), model)[0]


def infer_providers(providers, db):
    providers_data = sum([provider.get_all_faces_data() for provider in providers], [])
    db.add_complex_object(providers_data, many=True)
