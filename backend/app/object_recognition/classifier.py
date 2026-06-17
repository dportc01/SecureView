from app.camera.camera_interface import Frame
from dataclasses import dataclass
from pathlib import Path
import cv2


@dataclass
class Detection:
    class_id: int
    box: tuple[int, int, int, int]


class Clasiffier():
    def __init__(self):

        base_path = Path(__file__).resolve().parent / 'model'

        with open(base_path / 'object_detection_classes_coco.txt', 'r') as f:
            self.class_names = f.read().split('\n')

        self.detection_color = (31, 181, 38)
        self.model = cv2.dnn.readNet(
            str(base_path / 'frozen_inference_graph.pb'),
            str(base_path / 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt'),
            'TensorFlow'
        )

        self.interested_classes = [1]

    def classify(self, frame: Frame) -> list[Detection]:

        width = frame.width
        height = frame.height

        blob = cv2.dnn.blobFromImage(
            image=frame.data,
            size=(300, 300),
            mean=(104, 117, 123),
            swapRB=True
        )

        self.model.setInput(blob)
        outputs = self.model.forward()

        detections: list[Detection] = []

        for detection in outputs[0, 0, :, :]:
            class_id = detection[1]
            if class_id not in self.interested_classes:
                pass

            confidence = detection[2]
            if confidence > 0.6:
                box_x = detection[3] * width
                box_y = detection[4] * height
                box_width = detection[5] * width
                box_height = detection[6] * height
                detections.append(Detection(
                    class_id=class_id,
                    box=(box_x, box_y, box_width, box_height),
                ))

        return detections

    def draw(self, frame: Frame, detections: list[Detection]):
        for detect in detections:
            x1, y1, x2, y2 = detect.box
            class_name = self.class_names[int(detect.class_id)-1]

            cv2.rectangle(
                    frame.data,
                    (x1, y1),
                    (x2, y2),
                    self.detection_color,
                    thickness=1
                )
            cv2.putText(
                frame.data,
                class_name,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (20, 20, 20), 2)
