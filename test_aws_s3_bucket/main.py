import boto3
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

def list_buckets(client: any) -> list:
    response = client.list_buckets()
    return response["Buckets"]


def get_policy(client: any, bucket: str) -> str:
    response = client.get_bucket_policy(Bucket=bucket)
    return response["Policy"]


def list_objects(client: any, bucket: str, prefix: str = "", items: int = 100) -> list:
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=items)
    return (response["IsTruncated"], response["Contents"])


def get_object_data(client: any, bucket: str, file: str) -> bytes:
    response = client.get_object(Bucket=bucket, Key=file)
    return response["Body"].read()


def put_object_data(client: any, bucket: str, file: str, data: bytes) -> dict:
    return client.put_object(Bucket=bucket, Key=file, Body=data)


try:
    client = boto3.client("s3")
    bucket_name = "testing"
    print(list_objects(client, bucket_name))

except Exception:
    traceback.print_exc()
