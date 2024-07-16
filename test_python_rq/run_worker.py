import os
import rq
import sys
import redis
import traceback


try:
    with redis.Redis(
        host=os.environ.get("REDIS_HOST", "127.0.0.1"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        password=os.environ.get("REDIS_PASS"),
        db=int(os.environ.get("REDIS_DB", 0))
    ) as client:
        with rq.Connection(client) as connection:
            test_q = rq.Queue(name="testing", connection=connection)
            print("{} has {} messages.".format(test_q.name, test_q.count))

            worker = rq.Worker(test_q)
            print("Create worker: {}".format(worker.name))
            worker.work()

except Exception:
    traceback.print_exc()
    sys.exit(1)
