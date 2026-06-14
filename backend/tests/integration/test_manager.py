import time
import logging
import pytest
from multiprocessing import Queue, Process
from app.workers.manager import start_camera_workers, wait_and_terminate_camera_workeres
from app.messaging import BusInterface, MutiprocessingBus
from app.discovery import CameraType, CameraData


@pytest.fixture
def queues_setup():
    queues = [Queue()]
    res_queue = Queue()
    return queues, res_queue


def test_manager_star_terminate_cycle(queues_setup):

    queues, res_queue = queues_setup
    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]

    bus = MutiprocessingBus(queues, res_queue)

    processes = start_camera_workers(cameras_data, bus)

    assert len(processes) == 1
    for p in processes:
        assert p.is_alive()

    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    wait_and_terminate_camera_workeres(processes)

    for p in processes:
        assert not p.is_alive()

    aux_procc.join()


def test_empty_data_manager(queues_setup):

    queues, res_queue = queues_setup
    cameras_data: list[CameraData] = []

    bus = MutiprocessingBus(queues, res_queue)

    processses = start_camera_workers(cameras_data, bus)

    assert len(processses) == 0


def simulate_external_terminate(bus: BusInterface):
    time.sleep(1)
    logging.warning("Attempt termination:")
    bus.send_terminate()
