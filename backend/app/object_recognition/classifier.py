from app.camera.camera_interface import Frame
import cv2


class Clasiffier():
    def __init__(self):
        with open('./model/object_detection_classes_coco.txt', 'r') as f:
            self.class_names = f.read().split('\n')

        self.detection_color = (31, 181, 38)
        self.model = cv2.dnn.readNet(
            './MobileNetSSD/frozen_inference_graph.pb',
            './MobileNetSSD/ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt',
            'TensorFlow'
        )

        self.interested_classes = [1]

    def classify(self, frame: Frame):

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
                class_name = self.class_names[int(class_id)-1]
                cv2.rectangle(
                    frame.data,
                    (int(box_x), int(box_y)),
                    (int(box_width), int(box_height)),
                    self.detection_color,
                    thickness=1
                )
                cv2.putText(
                    frame.data,
                    class_name,
                    (int(box_x), int(box_y - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (20, 20, 20), 2)
