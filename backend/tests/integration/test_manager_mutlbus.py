# This tests are mostly falky and depend on the computer processing power

import time
import logging
from multiprocessing import Process
from app.workers import start_workers, wait_and_terminate_workeres, ManagerControlParams
from app.messaging import BusInterface, MutiprocessingBus
from app.notification import MockNotification
from app.discovery import CameraType, CameraData
from app.config import MAX_FRAME_QUEUE_SIZE


def test_manager_star_terminate_cycle():

    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]

    bus = MutiprocessingBus(cameras_data)
    notifier = MockNotification()

    control_params = start_workers(cameras_data, bus, notifier)

    assert len(control_params.camera_processes) == 1
    for p in control_params.camera_processes:
        assert p.is_alive()

    assert control_params.notif_thread.is_alive()

    terminate_workers(control_params, bus)


def test_empty_data_manager():

    cameras_data: list[CameraData] = []

    bus = MutiprocessingBus(cameras_data)
    notifier = MockNotification()

    control_params = start_workers(cameras_data, bus, notifier)

    assert len(control_params.camera_processes) == 0


def test_camera_worker_start():

    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]

    bus = MutiprocessingBus(cameras_data)
    notifier = MockNotification()

    control_params = start_workers(cameras_data, bus, notifier)

    bus.send_start(0)
    # Warm-up time
    time.sleep(0.4)

    frame1 = bus.read_frame(0)
    time.sleep(0.1)
    frame2 = bus.read_frame(0)

    terminate_workers(control_params, bus)

    assert frame1 != frame2


def test_camera_worker_stop():

    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]

    bus = MutiprocessingBus(cameras_data)
    notifier = MockNotification()

    control_params = start_workers(cameras_data, bus, notifier)

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
    for i in range(MAX_FRAME_QUEUE_SIZE):
        frame = bus.read_frame(0)
        if bus is None:
            break

    frame = bus.read_frame(0)
    terminate_workers(control_params, bus)

    assert frame is None


def terminate_workers(control_params: ManagerControlParams, bus: BusInterface):
    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    logging.warning("Waiting for camera termination:")
    wait_and_terminate_workeres(control_params)

    for p in control_params.camera_processes:
        assert not p.is_alive()

    aux_procc.join()


# Helper method to avoid deadlock
def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    logging.warning("Attempt termination:")
    bus.send_terminate()
