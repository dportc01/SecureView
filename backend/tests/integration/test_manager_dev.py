# This tests are mostly falky and depend on the computer processing power

import time
import logging
from multiprocessing import Process
from app.workers.manager import (
    start_camera_workers,
    wait_and_terminate_camera_workeres
)
from app.messaging import BusInterface, MutiprocessingBus
from app.discovery import CameraType, CameraData
from app.config import MAX_QUEUE_SIZE


def test_manager_star_terminate_cycle():

    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]

    bus = MutiprocessingBus(cameras_data)

    processes = start_camera_workers(cameras_data, bus)

    assert len(processes) == 1
    for p in processes:
        assert p.is_alive()

    terminate_workers(processes, bus)


def test_empty_data_manager():

    cameras_data: list[CameraData] = []

    bus = MutiprocessingBus(cameras_data)

    processses = start_camera_workers(cameras_data, bus)

    assert len(processses) == 0


def test_camera_worker_start():

    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]

    bus = MutiprocessingBus(cameras_data)

    processes = start_camera_workers(cameras_data, bus)

    bus.send_start(0)
    # Warm-up time
    time.sleep(0.4)

    frame1 = bus.read_frame(0)
    time.sleep(0.1)
    frame2 = bus.read_frame(0)

    terminate_workers(processes, bus)

    assert frame1 != frame2


def test_camera_worker_stop():

    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]

    bus = MutiprocessingBus(cameras_data)

    processes = start_camera_workers(cameras_data, bus)

    bus.send_start(0)

    # Wait to produce at least 60 frames
    time.sleep(0.6)
    bus.send_stop(0)

    # Retry until stop response recieved
    bus.read_response()  # Empty start response message
    for i in range(5):
        res = bus.read_response()
        if res is not None:
            break
        time.sleep(0.1)

    assert res is not None

    # Empty queue
    for i in range(MAX_QUEUE_SIZE):
        frame = bus.read_frame(0)
        if bus is None:
            break

    frame = bus.read_frame(0)
    terminate_workers(processes, bus)

    assert frame is None


def terminate_workers(processes, bus: BusInterface):
    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    logging.warning("Waiting for camera termination:")
    wait_and_terminate_camera_workeres(processes)

    for p in processes:
        assert not p.is_alive()

    aux_procc.join()


# Helper method to avoid deadlock
def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    logging.warning("Attempt termination:")
    bus.send_terminate()
