from typing import List

import numpy as np

from models.UserFace import UserFace


class IFaceCompare:
    async def compare_faces(self, faces_data: List[UserFace], encoding: np.array) -> UserFace:
        raise NotImplementedError
