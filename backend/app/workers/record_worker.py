from multiprocessing import Queue
from app.record import Recorder, Command, Type
from app.logging.loggers import get_record_logger


def record_worker(recoder: Recorder, queue: Queue, id: int):
    alive = True
    logger = get_record_logger(id)

    while alive:
        order: Command = (
            queue.get()
        )  # Process should stay dormant when no recording is happening
        if order.type == Type.FRAME:
            if order.frame is None:
                logger.error("Need initial frame to determine size before recording")
            else:
                h, w = order.frame.shape[:2]
                try:
                    recoder.start_record(camera_id=id, height=h, width=w)
                    logger.info("Started recording")
                except RuntimeError as e:
                    logger.exception(e)
                    order.frame = None  # Drop fram when file hasn't opened

                while order.type != Type.STOP and order.type != Type.TERMINATE:

                    if order.type == Type.FRAME:
                        if order.frame is None:
                            logger.error("Couldn't record, missing frame")
                        else:
                            recoder.insert_frame(order.frame)

                    order = queue.get()

            recoder.stop_record()
            logger.info("Stopped recording")

        if order.type == Type.TERMINATE:
            alive = False
            logger.info("Terminating recorder")

    return
