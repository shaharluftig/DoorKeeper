from typing import List

import face_recognition
import numpy as np

from config.door_keeper_config import THRESHOLD
from face_compares.IFaceCompare import IFaceCompare
from face_utils import get_generated_userface
from models.UserFace import UserFace


class FaceDistanceCompare(IFaceCompare):
    def __init__(self, threshold=THRESHOLD):
        self.threshold = threshold

    async def compare_faces(self, faces_data: List[UserFace], encoding: np.array) -> UserFace:
        distances = [1 - distance for distance in
                     face_recognition.face_distance([person.encoding for person in faces_data], encoding)]
        faces_data_distances = dict(zip(distances, faces_data))
        best_match = max(faces_data_distances, key=float)
        if best_match >= self.threshold:
            return faces_data_distances[best_match]
        return await get_generated_userface()
