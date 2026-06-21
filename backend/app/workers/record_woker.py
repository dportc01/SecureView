from multiprocessing import Queue
from record import Recorder, Command, Type
from app.logging.loggers import get_record_logger


def record_woker(recoder: Recorder, queue: Queue, id: int):
    alive = True
    logger = get_record_logger(id)

    while alive:
        order: Command = queue.get()  # Process should stay dormant when no recording is happening
        if order.type == Type.START:
            while order.type != Type.STOP and order.type != Type.TERMINATE:
                recoder.start_record()
                logger.info("Started recording")

                order = queue.get()

                if order.type == Type.FRAME:
                    if order.frame is None:
                        logger.error("Couldn't record, missing frame")
                    else:
                        recoder.insert_frame(order.frame)

            recoder.stop_record()

        if order.type == Type.TERMINATE:
            alive = False

    return
