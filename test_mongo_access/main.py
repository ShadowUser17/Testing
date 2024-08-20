# https://pymongo.readthedocs.io/en/stable/tutorial.html
import os
import pymongo
import traceback


try:
    client = pymongo.MongoClient(
        host=os.environ.get("MONGO_HOST", "127.0.0.1"),
        port=int(os.environ.get("MONGO_PORT", "27017")),
        username=os.environ.get("MONGO_USER", "root"),
        password=os.environ.get("MONGO_PASS", "testing")
    )

    for item in client.list_database_names():
        print(item)

except Exception:
    traceback.print_exc()
