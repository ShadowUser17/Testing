import os
import rq
import sys
import time
import redis
import funcs
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

        stats = {}
        q_name = test_q.name

        while True:
            job = test_q.enqueue(funcs.get_func())
            f_name = str(job.func_name)

            if stats.get(f_name):
                stats[f_name] += 1
            else:
                stats[f_name] = 1

            print("Put: {} to {}: {}".format(f_name, q_name, stats[f_name]))
            time.sleep(2)

except Exception:
    traceback.print_exc()
    sys.exit(1)
