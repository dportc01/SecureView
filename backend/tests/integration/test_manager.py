import time
import logging
from multiprocessing import Queue, Process
from app.workers.manager import start_camera_workers, wait_and_terminate_camera_workeres
from app.messaging import BusInterface, MutiprocessingBus
from app.discovery import CameraType, CameraData


def test_manager_star_terminate_cycle():

    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]
    queues = [Queue()]

    bus = MutiprocessingBus(queues)

    processes = start_camera_workers(cameras_data, bus)

    assert len(processes) == 1
    for p in processes:
        assert p.is_alive()

    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    wait_and_terminate_camera_workeres(processes)

    for p in processes:
        assert p.is_alive() != True

    aux_procc.join()

def simulate_external_terminate(bus: BusInterface):
    time.sleep(1)
    logging.warning("Attempt termination:")
    bus.send_terminate()
