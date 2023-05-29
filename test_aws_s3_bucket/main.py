import sys
import boto3
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

try:
    bucket_name = 'testing'
    client = boto3.client('s3')

    bucket_items = client.list_objects_v2(
        Bucket=bucket_name,
        MaxKeys=100,
        FetchOwner=True
    )

    for key_name in map(lambda item: item['Key'], bucket_items.get('Contents', [])):
        response = client.get_object(
            Bucket=bucket_name,
            Key=key_name
        )

        print('{} ({})'.format(key_name, response['ContentType']))
        print('Body:', response['Body'].read().decode())

except Exception:
    traceback.print_exc()
    sys.exit(1)
