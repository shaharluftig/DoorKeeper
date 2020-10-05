from collections import Counter

import cv2
import face_recognition
import imutils
import numpy as np

from Config import THRESHOLD


class FaceException(Exception):
    pass


def prepare_image(path: str, model="hog"):
    image = cv2.imread(path, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(image, model=model)
    encoding = face_recognition.face_encodings(image, boxes)
    if len(encoding) == 0:
        raise FaceException(f"Face not found at {path}")
    if len(encoding) > 1:
        raise FaceException(f"Multiply faces found at {path}, Try again")
    return encoding[0]


def determine_persons(matches: list, number_of_faces: int):
    return Counter(matches).most_common(number_of_faces)


def compare_faces(faces_data: dict, encoding: np.array):
    distances = {person:
                     1 - float(face_recognition.face_distance(np.array([faces_data[person]]), encoding))
                 for person in faces_data}
    best_match = max(distances, key=distances.get)
    if distances[best_match] >= THRESHOLD:
        return best_match


def get_frame_encoding(frame: np.array, model="hog"):
    rgb = imutils.resize(frame, width=750)
    boxes = face_recognition.face_locations(rgb, model=model)
    encodings = face_recognition.face_encodings(rgb, boxes)
    return encodings


def save_frame_to_disk(file_name, frame: np.array):
    if frame is not None:
        cv2.imwrite(file_name, frame)
