from Models.UserFace import UserFace


class IProvider:
    def get_faces_data(self) -> [UserFace]:
        raise NotImplementedError
