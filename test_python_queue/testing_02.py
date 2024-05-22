import sys
import time
import typing
import traceback
import threading


class Data:
    def __init__(self, data: typing.Iterable = []) -> None:
        self._data = data
        self._lock = threading.Lock()

    def get(self) -> typing.Any:
        with self._lock:
            return self._data.pop()

    def put(self, item: typing.Any) -> None:
        with self._lock:
            self._data.append(item)

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def __iter__(self) -> typing.Iterable:
        return self

    def __next__(self) -> typing.Any:
        with self._lock:
            if len(self._data) > 0:
                return self._data.pop()

            else:
                raise StopIteration()


def data_generator(data: Data) -> None:
    for item in range(0, 10):
        data.put(item)
        time.sleep(1)


def data_printer(data: Data) -> None:
    while True:
        for item in data:
            print("Data:", item)


try:
    data = Data()
    workers = []

    workers.append(threading.Thread(target=data_generator, args=(data,)))
    workers.append(threading.Thread(target=data_printer, args=(data,)))

    for thr in workers:
        thr.start()

    for thr in workers:
        thr.join()

except Exception:
    traceback.print_exc()
    sys.exit(1)
