import logging
import time
from datetime import datetime, time as dt_time
from queue import Queue
from app.config import NOTIF_COOLDOWN, RECORD_TIMES, RecordTime
from app.discovery import CameraData
from app.camera.factory import build_camera
from app.camera.frame import Frame
from app.messaging import BusInterface, Action
from app.notification import Command as notif_cmd, Type as notif_type
from app.object_recognition.classifier import Clasiffier


# TODO: If camera is alredy stopped change the respond message
def camera_woker(camera_data: CameraData, bus: BusInterface, notif_queue: Queue):

    camera = build_camera(camera_data)
    classifier = Clasiffier()
    alive = True
    last_notif_time: float = 0.0
    record_times = RECORD_TIMES.get(camera_data['id'])

    try:
        while alive:
            order = bus.cam_recv(camera_data['id'])

            if (order == Action.START):
                bus.respond(f"Starting recording on camera: {camera_data['id']}")
                frame_stream = camera.start_capture()
                for frame in frame_stream:
                    last_notif_time = _process_frame(
                        bus,
                        frame,
                        classifier,
                        notif_queue,
                        camera_data['id'],
                        last_notif_time,
                        record_times
                    )

                    # Breack loop check
                    order = bus.cam_recv(camera_data['id'])
                    if order == Action.STOP or order == Action.TERMINATE:
                        break

            if (order == Action.STOP):
                bus.respond(f"Stoping recording on camera: {camera_data['id']}")
                camera.stop_capture()

            if (order == Action.TERMINATE):
                bus.respond(f"Terminating camera: {camera_data['id']}")
                logging.info(f"Terminating camera {camera_data['id']}")
                alive = False

        return
    finally:
        camera.stop_capture()
        bus.close()


def _process_frame(
    bus: BusInterface,
    frame: Frame,
    classifier: Clasiffier,
    notif_queue: Queue,
    camera_id: int,
    last_notif_time: float,
    record_times: RecordTime | None,
) -> float:

    now = time.time()
    now_time = datetime.now().time()

    # Object detection
    detections = classifier.classify(frame)
    classifier.draw(frame, detections)

    # Record frame
    if record_times:
        if _is_between(now_time, record_times.start, record_times.end):
            ...

    # JPG img encoding
    img_frame = frame.to_bytes()

    # Notification if person detected
    try:
        if detections and (now - last_notif_time >= NOTIF_COOLDOWN):
            for detect in detections:
                notif_queue.put_nowait(
                    notif_cmd(
                        notif_type.IMAGE,
                        f"{detect.class_name} detected on camera: {camera_id}",
                        img_frame
                    )
                )
            last_notif_time = now
    except Exception:
        logging.error("Couldn't put notification on queue")

    # Sending to Flask server
    bus.write_frame(camera_id, img_frame)

    return last_notif_time


def _is_between(now: dt_time, start: dt_time, end: dt_time):
    if start <= end:
        return start <= now <= end
    else:
        return now >= start or now <= end
