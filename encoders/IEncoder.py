import numpy as np


class IEncoder:
    def encode(self, image) -> np.array:
        raise NotImplementedError
