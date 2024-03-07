# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html
import sys
import boto3
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY


try:
    client = boto3.client("eks")

except Exception:
    traceback.print_exc()
    sys.exit(1)
