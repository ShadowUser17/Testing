import sys
import time
import queue
import threading
import traceback


def data_generator(src: queue.Queue) -> None:
    while True:
        item = int(time.time())
        print("data_generator:", item)
        src.put(item)
        time.sleep(2)


def data_processor(src: queue.Queue, dst: queue.Queue) -> None:
    while True:
        item = src.get()
        print("data_processor:", item)
        dst.put(item)
        src.task_done()


def data_printer(dst: queue.Queue) -> None:
    while True:
        item = dst.get()
        print("data_printer:", item)
        dst.task_done()


try:
    src = queue.Queue()
    dst = queue.Queue()
    workers = []

    workers.append(threading.Thread(target=data_generator, args=(src,)))
    workers.append(threading.Thread(target=data_processor, args=(src, dst,)))
    workers.append(threading.Thread(target=data_printer, args=(dst,)))

    for thr in workers:
        thr.start()

    for thr in workers:
        thr.join()

except Exception:
    traceback.print_exc()
    sys.exit(1)
