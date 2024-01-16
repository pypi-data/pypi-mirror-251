import os
from deepface import DeepFace
from deepface.commons import distance as dst
import uuid
import cv2

class FaceRecognitionSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(FaceRecognitionSingleton, cls).__new__(cls)
            cls._instance.models = [
                "VGG-Face",
                "Facenet",
                "Facenet512",
                "OpenFace",
                "DeepFace",
                "DeepID",
                "ArcFace",
                "Dlib",
                "SFace",
            ]
            cls._instance.backends = ["retinaface", "dlib"]
        return cls._instance

    def get_embedding_vector(self, path: str, detector: str):
        embed = []
        data = DeepFace.represent(
            path,
            model_name=self.models[2],
            enforce_detection=True,
            detector_backend=detector,
        )
        for imgdata in data:
            embed.append(imgdata["embedding"])
        return embed

    def extract_face(self, path: str, detector: str):
        data = DeepFace.represent(
            path,
            model_name=self.models[2],
            enforce_detection=True,
            detector_backend=detector,
        )
        return data


    def generate_faces_image(self, path: str, album_dir: str, detector: str):
        image_names = []
        extracted_face = DeepFace.extract_faces(
            img_path=path,
            enforce_detection=True,
            detector_backend=detector,
            align=True,
        )
        for idx, face in enumerate(extracted_face):
            im = cv2.cvtColor(face["face"] * 255, cv2.COLOR_BGR2RGB)
            name = uuid.uuid4()
            cv2.imwrite(os.path.join(album_dir, f"{name}.jpg"), im)
            image_names.append(os.path.join(album_dir, f"{name}.jpg"))
        return image_names
