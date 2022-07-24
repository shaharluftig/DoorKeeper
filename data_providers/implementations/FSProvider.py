import os

from loggers.implementations.PythonLogger import PythonLogger

import face_utils
from data_providers.IProvider import IProvider
from encoders.IEncoder import IEncoder
from encoders.implementations.FaceEncoder import FaceEncoder
from models.UserFace import UserFace

logger = PythonLogger()


class FSProvider(IProvider):
    def __init__(self, path="./images", encoder: IEncoder = FaceEncoder()):
        self.encoder = encoder
        self.path = path

    @logger.session_log
    def get_all_faces_data(self) -> [UserFace]:
        listdir = os.listdir(self.path)
        images = [file for file in listdir if os.path.isfile(f"{self.path}/{file}")]
        faces_data = [self.get_face_data(f"{self.path}/{image}") for image in images]
        return faces_data

    def get_face_data(self, image_path) -> [UserFace]:
        face_data = UserFace(image_path.split("/")[-1].split(".")[0], image_path,
                             face_utils.infer_fs_image(image_path, self.encoder).tolist(),
                             image_path)
        return face_data
