from pathlib import Path
import cv2

from app.object_recognition.classifier import Clasiffier
from app.camera import Frame


def test_classifier():
    base_path = Path(__file__).resolve().parent / "assets"
    image = cv2.imread(str(base_path / "image.jpg"))

    if image is None:
        raise ValueError("Test image not found or unreadable")

    height, width = image.shape[:2]
    classifier = Clasiffier()

    detections = classifier.classify(
        Frame(
            data=image,
            width=width,
            height=height,
        )
    )

    assert len(detections) == 2
    assert detections[1].class_name == "person"
    assert detections[1].class_name == "person"
