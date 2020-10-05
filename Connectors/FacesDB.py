import os

import numpy as np

import FaceUtils
from Connectors.RedisConnector import RedisConnector
from Logging.PythonLogger import PythonLogger

logger = PythonLogger()


class FacesDB(RedisConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @logger.session_log
    def collect_all_data(self):
        faces_data = super(FacesDB, self).collect_all_data()
        for key in faces_data:
            faces_data[key] = np.array(faces_data[key])
        return faces_data

    @logger.session_log
    def infer_image_folder(self, path: str, model="hog"):
        for image in os.listdir(path):
            image_path = path + "/" + image
            logger.log(f"Inferring : {image_path}")
            encoding = FaceUtils.prepare_image(image_path, model).tolist()
            image_name = image.split(".")[0]
            self.add_complex_object(image_name, encoding)
