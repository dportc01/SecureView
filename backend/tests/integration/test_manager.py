import time
import logging
from multiprocessing import Process
from app.workers.manager import (
    start_camera_workers,
    wait_and_terminate_camera_workeres
)
from app.messaging import BusInterface, MutiprocessingBus
from app.discovery import CameraType, CameraData


def test_manager_star_terminate_cycle():

    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]

    bus = MutiprocessingBus(len(cameras_data))

    processes = start_camera_workers(cameras_data, bus)

    assert len(processes) == 1
    for p in processes:
        assert p.is_alive()

    terminate_workers(processes, bus)


def test_empty_data_manager():

    cameras_data: list[CameraData] = []

    bus = MutiprocessingBus(len(cameras_data))

    processses = start_camera_workers(cameras_data, bus)

    assert len(processses) == 0


def test_camera_worker_coms():

    camera_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]

    bus = MutiprocessingBus(len(camera_data))

    processes = start_camera_workers(camera_data, bus)

    bus.send_start(0)

    time.sleep(10)
    frame = bus.read_frame(0)

    assert frame in [b"frame1", b"frame2", b"frame3"]

    terminate_workers(processes, bus)


def terminate_workers(processes, bus):
    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    wait_and_terminate_camera_workeres(processes)

    for p in processes:
        assert not p.is_alive()

    aux_procc.join()


# Helper method to avoid deadlock
def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    logging.warning("Attempt termination:")
    bus.send_terminate()
