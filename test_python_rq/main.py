import os
import rq
import sys
import math
import time
import redis
import traceback


try:
    with redis.Redis(
        host=os.environ.get("REDIS_HOST", "127.0.0.1"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        password=os.environ.get("REDIS_PASS"),
        db=int(os.environ.get("REDIS_DB", 0))
    ) as client:
        # print(client.info("server"))

        test_q = rq.Queue(name="testing", connection=client)
        print("{} has {} messages.".format(test_q.name, test_q.count))

        if not test_q.count:
            for item in range(1, 10):
                job = test_q.enqueue(math.pow, item, 10)
                time.sleep(2)
                print(job.return_value())

        print("{} has {} messages.".format(test_q.name, test_q.count))

except Exception:
    traceback.print_exc()
    sys.exit(1)
