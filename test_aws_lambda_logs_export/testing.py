import traceback
import boto3
import time


def create_log_group(client: any, log_group: str, log_retention: int = 30) -> None:
    client.create_log_group(
        logGroupName=log_group,
        tags={"Name": log_group}
    )

    client.put_retention_policy(
        logGroupName=log_group,
        retentionInDays=log_retention
    )


def describe_log_groups(client: any, log_group: str) -> list:
    resp = client.describe_log_groups(
        logGroupNamePrefix=log_group
    )

    return resp.get("logGroups", [])


def put_subscription_filter(client: any, log_group: str, target_arn: str) -> None:
    client.put_subscription_filter(
        logGroupName=log_group,
        filterName=log_group,
        filterPattern='" "',
        destinationArn=target_arn
    )


def create_log_stream(client: any, log_group: str, log_stream: str) -> None:
    client.create_log_stream(
        logGroupName=log_group,
        logStreamName=log_stream
    )


def put_log_events(client: any, log_group: str, log_stream: str, message: str) -> None:
    client.put_log_events(
        logGroupName=log_group, logStreamName=log_stream,
        logEvents=[{"timestamp": int(round(time.time() * 1000)), "message": message}]
    )


def delete_log_group(client: any, log_group: str) -> None:
    client.delete_log_group(logGroupName=log_group)


try:
    client = boto3.client("logs")

    for log_id in range(1, 4):
        log_group = "testing-{}".format(log_id)
        put_log_events(client, log_group, "data", "request_id: {}".format(time.time_ns()))

except Exception:
    traceback.print_exc()
