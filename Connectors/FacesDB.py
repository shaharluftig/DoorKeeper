import os

import numpy as np

import FaceUtils
from Connectors.RedisConnector import RedisConnector


class FacesDB(RedisConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect_all_data(self):
        faces_data = super(FacesDB, self).collect_all_data()
        for key in faces_data:
            faces_data[key] = np.array(faces_data[key])
        return faces_data

    def infer_image_folder(self, path, model="hog"):
        for image in os.listdir(path):
            encoding = FaceUtils.prepare_image(path + "/" + image, model).tolist()
            image_name = image.split(".")[0]
            self.add_complex_object(image_name, encoding)
