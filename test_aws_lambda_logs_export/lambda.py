from urllib import parse as urllib
from urllib import request

import traceback
import base64
import boto3
import gzip
import json
import os


def get_log_event_data(event):
    compressed_data = base64.b64decode(event["awslogs"]["data"])
    json_data = gzip.decompress(compressed_data)
    return json.loads(json_data)


def get_log_group_labels(log_group):
    aws_region = os.environ.get("AWS_REGION")
    cloudwatch_logs = boto3.client("logs", region_name=aws_region)

    try:
        response = cloudwatch_logs.list_tags_log_group(logGroupName=log_group)
        src_tags = response["tags"].items()
        dst_tags = dict()

        for (key, val) in src_tags:
            dst_tags[key.lower()] = val

        return dst_tags

    except Exception:
        #traceback.print_exc()
        return {"Name": log_group}


def send_log_data_to_loki(log_data, log_labels):
    url = urllib.urljoin(
        base=os.environ.get("LOKI_ENDPOINT", "http://localhost:3100"),
        url="/loki/api/v1/push"
    )

    log_items = []
    for item in log_data["logEvents"]:
        log_time_ns = int(item["timestamp"]) * 1000000
        log_items.append([str(log_time_ns), item["message"]])

    payload = {
        "streams": [{
            "stream": log_labels,
            "values": log_items
        }]
    }

    req = request.Request(
        url=url, method="POST",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )

    try:
        with request.urlopen(req) as client:
            return {"status": client.status, "reason": client.reason}

    except Exception:
        traceback.print_exc()
        return {"status": 0, "reason": ""}


def lambda_handler(event, context):
    log_data = get_log_event_data(event)
    log_labels = get_log_group_labels(log_data["logGroup"])
    response = send_log_data_to_loki(log_data, log_labels)

    return {
        "statusCode": response["status"],
        "body": response["reason"]
    }
