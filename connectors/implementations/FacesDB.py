import numpy as np

from config.constants import FULL_NAME, PK, ENCODING, PATH
from connectors.implementations.MongoConnector import MongoConnector
from loggers.implementations.PythonLogger import PythonLogger
from models.UserFace import UserFace

logger = PythonLogger()


class FacesDB(MongoConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @logger.session_log
    def collect_all_data(self) -> [UserFace]:
        data = super(FacesDB, self).collect_all_data()
        return [UserFace(item[FULL_NAME], item[PK], np.array(item[ENCODING]), item[PATH])
                for item in data]

    @logger.session_log
    def insert_all_data(self, user_faces: UserFace):
        return super(FacesDB, self).add_complex_object(user_faces, many=True)
