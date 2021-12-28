import os

import face_utils
from DataProviders.IProvider import IProvider
from Logging.PythonLogger import PythonLogger
from Models.UserFace import UserFace

logger = PythonLogger()


class FSProvider(IProvider):
    def __init__(self, path: str, model="hog"):
        self.path = path
        self.model = model

    @logger.session_log
    def get_faces_data(self) -> [UserFace]:
        faces_data = []
        for image in os.listdir(self.path):
            image_path = self.path + "/" + image
            logger.log(f"Inferring : {image_path}")
            encoding = face_utils.infer_fs_image(image_path, self.model).tolist()
            faces_data.append(UserFace(image.split(".")[0], image_path, encoding, image_path))
        return faces_data
