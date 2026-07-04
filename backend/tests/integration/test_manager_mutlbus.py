# This tests are mostly falky and depend on the computer processing power

import time
import logging
import pytest
from multiprocessing import Process, Queue

from tests.integration.mock_recorder import MockRecorder
from app.workers import start_workers, wait_and_terminate_workers, ManagerProcesses
from app.messaging import BusInterface, MultiprocessingBus
from app.notification import MockNotification
from app.discovery import CameraType, CameraData
from app.config import MAX_FRAME_QUEUE_SIZE


@pytest.fixture(scope="session")
def set_up_tests():
    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]
    bus = MultiprocessingBus(cameras_data)
    notifier = MockNotification()
    notif_queue = Queue()
    recorder = MockRecorder({"recording": False, "frame_received": False})
    record_queue = []
    for _ in range(len(cameras_data)):
        record_queue.append(Queue())

    control_params = start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=record_queue,
    )

    yield bus, control_params

    terminate_workers(control_params, bus, notif_queue, record_queue)


def test_manager_start_terminate_cycle(set_up_tests):

    _, control_params = set_up_tests

    assert len(control_params.camera_processes) == 1
    for p in control_params.camera_processes:
        assert p.is_alive()

    assert control_params.notif_thread.is_alive()


def test_empty_data_manager():

    cameras_data: list[CameraData] = []
    bus = MultiprocessingBus(cameras_data)
    notifier = MockNotification()
    notif_queue = Queue()
    recorder = MockRecorder({"recording": False, "frame_received": False})
    record_queue = []
    for _ in range(len(cameras_data)):
        record_queue.append(Queue())

    control_params = start_workers(
        cameras_data, bus, notifier, notif_queue, recorder, record_queue
    )

    assert len(control_params.camera_processes) == 0


def test_camera_worker_start(set_up_tests):

    bus, _ = set_up_tests

    bus.send_start(0)
    # Warm-up time
    time.sleep(0.8)

    frame1 = bus.read_frame(0)
    time.sleep(0.1)
    frame2 = bus.read_frame(0)

    assert frame1 != frame2


def test_camera_worker_stop(set_up_tests):

    bus, _ = set_up_tests

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

    assert frame is None


def terminate_workers(
    control_params: ManagerProcesses,
    bus: BusInterface,
    notif_queue: Queue,
    record_queue: list[Queue],
):
    aux_procc = Process(target=simulate_external_terminate, args=(bus,))
    aux_procc.start()

    logging.warning("Waiting for camera termination:")
    wait_and_terminate_workers(control_params, notif_queue, record_queue)

    for p in control_params.camera_processes:
        assert not p.is_alive()

    assert not control_params.notif_thread.is_alive()

    for p in control_params.record_processes:
        assert not p.is_alive()

    aux_procc.join()


# Helper method to avoid deadlock
def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    logging.warning("Attempt termination:")
    bus.send_terminate()
