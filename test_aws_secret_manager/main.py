import sys
import boto3
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY


def list_secrets(client: any, items: int) -> list:
    resp = client.list_secrets(MaxResults=items)
    return resp.get('SecretList', [])


def create_secret(client: any, name: str, data: str) -> tuple:
    resp = client.create_secret(Name=name, SecretString=data)
    return (resp['Name'], resp['ARN'])


def delete_secret(client: any, name: str) -> tuple:
    resp = client.delete_secret(SecretId=name)
    return (resp['Name'], resp['ARN'])


def get_value(client: any, name: str) -> str:
    resp = client.get_secret_value(SecretId=name)
    return resp.get('SecretString', '')


def set_value(client: any, name: str, data: str) -> str:
    resp = client.put_secret_value(SecretId=name, SecretString=data)
    return (resp['Name'], resp['ARN'])


try:
    client = boto3.client('secretsmanager')
    name = 'testing/data_v2'
    #print(create_secret(client, name, 'testing...'))
    #print(get_value(client, name))
    #print(set_value(client, name, '1..2..3..'))
    #print(get_value(client, name))
    #print(delete_secret(client, name))

except Exception:
    traceback.print_exc()
    sys.exit(1)
