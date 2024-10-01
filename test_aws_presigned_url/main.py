import boto3
import traceback

from urllib import request

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

def generate_presigned_url(client: any, bucket: str, file: str, method: str = "get", expire: int = 1000) -> str:
    '''
    method - <get | put>
    expire - The number of seconds.
    '''
    method = "get_object" if method == "get" else "put_object"
    return client.generate_presigned_url(
        ClientMethod=method, Params={"Bucket": bucket, "Key": file}, ExpiresIn=expire
    )


try:
    s3 = boto3.client("s3")
    bucket_name = "testing"
    bucket_file = "test_presigned_ur/1.txt"

    url = generate_presigned_url(s3, bucket_name, bucket_file, method="put")
    print(url)

    data = "Testing..."
    req = request.Request(method="PUT", url=url, data=data.encode())
    with request.urlopen(req) as http_client:
        print("PUT {}/{}:".format(bucket_name, bucket_file), http_client.status)

    # sts = boto3.client("sts")
    # credentials = sts.get_session_token(DurationSeconds=3600)

    url = generate_presigned_url(s3, bucket_name, bucket_file, method="get")
    print(url)

    with request.urlopen(url) as http_client:
        print("GET {}/{}:".format(bucket_name, bucket_file), http_client.read())

except Exception:
    traceback.print_exc()
