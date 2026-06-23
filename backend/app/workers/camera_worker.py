import time
import numpy as np
from datetime import datetime, time as dt_time
from queue import Queue, Full
from app.config import NOTIF_COOLDOWN, RECORD_TIMES, RecordTime
from app.discovery import CameraData
from app.camera.factory import build_camera
from app.camera.frame import Frame
from app.messaging import BusInterface, Action
from app.notification import (
    Command as NotifCmd,
    Type as NotifType
)
from app.record import (
    Command as RecCmd,
    Type as RecType
)
from app.object_recognition.classifier import Clasiffier
from app.logging.loggers import get_camera_logger
from logging import Logger


# TODO: If camera is alredy stopped change the respond message
def camera_woker(
    camera_data: CameraData,
    bus: BusInterface,
    notif_queue: Queue,
    record_queue: Queue,
):

    camera = build_camera(camera_data)
    logger = get_camera_logger(camera_data['id'])
    classifier = Clasiffier()
    last_notif_time: float = 0.0
    record_times = RECORD_TIMES.get(camera_data['id'])
    is_recording = False
    alive = True

    try:
        while alive:
            order = bus.cam_recv(camera_data['id'])

            if (order == Action.START):
                bus.respond(f"Starting recording on camera: {camera_data['id']}")
                frame_stream = camera.start_capture()
                for frame in frame_stream:
                    last_notif_time, is_recording = _process_frame(
                        camera_id=camera_data['id'],
                        logger=logger,
                        bus=bus,
                        frame=frame,
                        classifier=classifier,
                        notif_queue=notif_queue,
                        last_notif_time=last_notif_time,
                        record_queue=record_queue,
                        record_times=record_times,
                        is_recording=is_recording,
                    )

                    # Breack loop check
                    order = bus.cam_recv(camera_data['id'])
                    if order == Action.STOP or order == Action.TERMINATE:
                        break

            if (order == Action.STOP):
                bus.respond(f"Stoping recording on camera: {camera_data['id']}")
                camera.stop_capture()
                record_queue.put(RecCmd(RecType.STOP, None))

            if (order == Action.TERMINATE):
                bus.respond(f"Terminating camera: {camera_data['id']}")
                logger.info(f"Terminating camera {camera_data['id']}")
                alive = False

        return
    finally:
        camera.stop_capture()
        bus.close()


def _process_frame(
    camera_id: int,
    logger: Logger,
    bus: BusInterface,
    frame: Frame,
    classifier: Clasiffier,
    notif_queue: Queue,
    last_notif_time: float,
    record_queue: Queue,
    record_times: RecordTime | None,
    is_recording: bool
) -> tuple[float, bool]:

    now = time.time()
    now_dt = datetime.now().time()

    # Object detection
    detections = classifier.classify(frame)
    classifier.draw(frame, detections)

    # Record frame
    if record_times:
        is_recording = _record_frame(
            now=now_dt,
            start=record_times.start,
            end=record_times.end,
            record_queue=record_queue,
            is_recording=is_recording,
            frame=frame.data
        )

    # JPG img encoding
    img_frame = frame.to_bytes()

    # Notification if person detected
    try:
        if detections and (now - last_notif_time >= NOTIF_COOLDOWN):
            for detect in detections:
                notif_queue.put_nowait(
                    NotifCmd(
                        NotifType.IMAGE,
                        f"{detect.class_name} detected on camera: {camera_id}",
                        img_frame
                    )
                )
            last_notif_time = now
    except Exception:
        logger.error("Couldn't put notification on queue")

    # Sending to Flask server
    bus.write_frame(camera_id, img_frame)

    return last_notif_time, is_recording


def _record_frame(
        now: dt_time,
        start: dt_time,
        end: dt_time,
        record_queue: Queue,
        is_recording: bool,
        frame: np.ndarray
) -> bool:

    if _is_between(now, start, end):
        if not is_recording:
            is_recording = True

        try:
            record_queue.put_nowait(RecCmd(RecType.FRAME, frame))
        except Full:
            pass  # If full drop frame
    else:
        if is_recording:
            record_queue.put(RecCmd(RecType.STOP, None))
            is_recording = False

    return is_recording


def _is_between(now: dt_time, start: dt_time, end: dt_time):
    if start <= end:
        return start <= now <= end
    else:
        return now >= start or now <= end
