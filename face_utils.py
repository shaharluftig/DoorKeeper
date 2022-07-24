import secrets
from collections import Counter

import cv2
import face_recognition
import numpy as np

from config.door_keeper_config import THRESHOLD
from encoders.IEncoder import IEncoder
from loggers.implementations.PythonLogger import PythonLogger
from models.UserFace import UserFace

logger = PythonLogger()


class VideoStreamException(Exception):
    """Raised when VideoStream is unreachable """
    pass


def show_image(image):
    cv2.imshow("face", image)
    cv2.waitKey(0)


def determine_persons(matches: list, number_of_faces: int):
    return Counter(matches).most_common(number_of_faces)


async def compare_faces(faces_data: list, encoding: np.array) -> UserFace:
    distances = [1 - distance for distance in
                 face_recognition.face_distance([person.encoding for person in faces_data], encoding)]
    faces_data_distances = dict(zip(distances, faces_data))
    best_match = max(faces_data_distances, key=float)
    if best_match >= THRESHOLD:
        return faces_data_distances[best_match]
    return await get_generated_userface()


async def get_generated_userface() -> UserFace:
    name = secrets.token_urlsafe(7)
    return UserFace(full_name=f"unknown_{name}", pk=f"./Images/{name}.jpg", encoding=None,
                    path=f"./Images/{name}.jpg")


async def save_frame_to_disk(file_name: str, frame: np.array):
    if frame is not None:
        cv2.imwrite(file_name, frame)


def infer_fs_image(path: str, encoder: IEncoder) -> np.array:
    logger.log(f"Inferring {path}")
    return encoder.encode(cv2.imread(path, cv2.COLOR_BGR2RGB))[0]


def infer_providers(providers, db):
    providers_data = sum([provider.get_all_faces_data() for provider in providers], [])
    db.add_complex_object(providers_data, many=True)
