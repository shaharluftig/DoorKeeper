from models.UserFace import UserFace


class IProvider:
    def get_all_faces_data(self) -> [UserFace]:
        raise NotImplementedError
