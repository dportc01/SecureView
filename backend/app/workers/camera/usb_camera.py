import cv2


class Camera:
    def __init__(self, device_index: int = 0):
        self.device_index = device_index
        self.cap = cv2.VideoCapture(device_index)

    def get_camera_count(self) -> int:
        count = 0
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                count += 1
                cap.release()
        return count

    def generate_frames(self):
        while True:
            success, frame = self.cap.read()

            if not success:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes +
                b'\r\n'
            )
