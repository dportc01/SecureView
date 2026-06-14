import logging


def camera_logger(device_index: int):
    logger = logging.getLogger(f"CAMERA:{device_index}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler("cameras.log")
        formatter = logging.Formatter(
            "TIME: %(asctime)s - LEVEL: %(levelname)s - %(name)s - MESSAGE: %(message)s",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger