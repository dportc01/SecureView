from multiprocessing import Queue
from record import Recorder

def record_woker(recoder: Recorder, queue: Queue):
    alive = True

    while alive:
        order = queue.get_nowait()