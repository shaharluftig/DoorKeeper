import face_recognition
import imutils
import numpy as np

from encoders.IEncoder import IEncoder


class FaceEncoder(IEncoder):
    def __init__(self, number_of_times_to_upsample=2, model="hog"):
        self.model = model
        self.number_of_times_to_upsample = number_of_times_to_upsample

    def encode(self, image) -> np.array:
        rgb = imutils.resize(image, width=750)
        boxes = face_recognition.face_locations(rgb, self.number_of_times_to_upsample, model=self.model)
        encoding = face_recognition.face_encodings(rgb, boxes)
        return encoding
