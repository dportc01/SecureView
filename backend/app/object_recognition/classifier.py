from app.camera.camera_interface import Frame
import cv2


def Clasiffier():
    def __init__(self):
        with open('./model/object_detection_classes_coco.txt', 'r') as f:
            self.class_names = f.read().split('\n')

        self.person_color = (31, 181, 38)
        self.model = cv2.dnn.readNet(
            './MobileNetSSD/frozen_inference_graph.pb',
            './MobileNetSSD/ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt',
            'TensorFlow'
        )

    def classify(self, frame: Frame):

        width = frame.width
        height = frame.height

        blob = cv2.dnn.blobFromImage(
            image=frame.data,
            size=(300, 300),
            mean=(104, 117, 123),
            swapRB=True
        )
