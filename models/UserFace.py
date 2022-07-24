from dataclasses import dataclass

import numpy as np


@dataclass
class UserFace:
    """Class for keeping track of faces data."""
    full_name: str
    pk: str
    encoding: np.array
    path: str

    def __hash__(self):
        return hash(self.pk)

    def __str__(self):
        return f"{self.full_name}"
