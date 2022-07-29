import numpy as np

from config.constants import FULL_NAME, PK, ENCODING, PATH
from connectors.implementations.MongoConnector import MongoConnector
from models.UserFace import UserFace


class FacesDB(MongoConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect_all_data(self) -> [UserFace]:
        data = super(FacesDB, self).collect_all_data()
        return [UserFace(item[FULL_NAME], item[PK], np.array(item[ENCODING]), item[PATH])
                for item in data]

    def insert_all_data(self, user_faces: UserFace):
        return super(FacesDB, self).add_complex_object(user_faces, many=True)
