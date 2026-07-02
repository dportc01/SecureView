import logging

_file_handler = None


def get_camera_logger(device_index: int):
    logger = logging.getLogger(f"CAMERA:{device_index}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_get_file_handler())

    return logger


def get_notification_logger():
    logger = logging.getLogger("NOTIFIER")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_get_file_handler())

    return logger


def get_record_logger(device_index: int):
    logger = logging.getLogger(f"RECORD:{device_index}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_get_file_handler())

    return logger


def get_system_logger():
    logger = logging.getLogger("SYSTEM")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_get_file_handler())

    return logger


def get_files_logger():
    logger = logging.getLogger("FILES")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_get_file_handler())

    return logger


def _get_file_handler() -> logging.FileHandler:
    global _file_handler

    if _file_handler is None:
        _file_handler = logging.FileHandler("app.log")
        formatter = logging.Formatter(
            "TIME: %(asctime)s - LEVEL: %(levelname)s - %(name)s - MESSAGE: %(message)s",
        )
        _file_handler.setFormatter(formatter)

    if _file_handler is None:
        raise RuntimeError("Couldn't get logger file handler")

    return _file_handler
