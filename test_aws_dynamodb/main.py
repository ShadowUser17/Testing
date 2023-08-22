import boto3
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

def list_tables(client: any, items: int = 100) -> list:
    response = client.list_tables(Limit=items)
    return response["TableNames"]


def describe_table(client: any, table: str) -> dict:
    return client.describe_table(TableName=table)


def list_items(client: any, table: str, items: int = 200) -> list:
    response = client.scan(TableName=table, Limit=items)
    return (response["Items"], response["Count"])


try:
    client = boto3.client("dynamodb")
    print(list_tables(client))

except Exception:
    traceback.print_exc()
