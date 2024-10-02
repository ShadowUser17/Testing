import boto3
import traceback

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
    expire_in_sec = 129600
    bucket_name = "testing"
    bucket_file = "test_presigned_ur/1.txt"

    # sts = boto3.client("sts")
    # credentials = sts.get_session_token(DurationSeconds=expire_in_sec)
    # print(credentials)

    s3 = boto3.client("s3")
    url = generate_presigned_url(s3, bucket_name, bucket_file, method="get")
    print(url)

except Exception:
    traceback.print_exc()
