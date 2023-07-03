import sys
import boto3
import pathlib
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

secrets = {
    "testing/private_key": {"Binary": False, "File": "secrets/testing_key.pem"},
    "testing/public_key": {"Binary": False, "File": "secrets/testing_key.pub"},
}


def read_file(path: str, is_binary: bool) -> any:
    if is_binary:
        return pathlib.Path(path).read_bytes()

    else:
        return pathlib.Path(path).read_text()


def write_file(path: str, data: any, is_binary: bool) -> int:
    if is_binary:
        return pathlib.Path(path).write_bytes(data)

    else:
        return pathlib.Path(path).write_text(data)


def list_secrets(client: any, items: int = 30) -> list:
    resp = client.list_secrets(MaxResults=items)
    return (resp['SecretList'], resp['NextToken'])


def describe_secret(client: any, name: str) -> dict:
    try:
        return client.describe_secret(SecretId=name)

    except client.exceptions.ResourceNotFoundException:
        return {}


def create_secret(client: any, name: str, data: any, is_binary: bool) -> tuple:
    if is_binary:
        resp = client.create_secret(Name=name, SecretBinary=data)
        return (resp['Name'], resp['ARN'])

    else:
        resp = client.create_secret(Name=name, SecretString=data)
        return (resp['Name'], resp['ARN'])


def delete_secret(client: any, name: str, recovery: int = 30) -> tuple:
    resp = client.delete_secret(SecretId=name, RecoveryWindowInDays=recovery)
    return (resp['Name'], resp['DeletionDate'])


def restore_secret(client: any, name: str) -> tuple:
    resp = client.restore_secret(SecretId=name)
    return (resp['Name'], resp['ARN'])


def get_value(client: any, name: str) -> str:
    resp = client.get_secret_value(SecretId=name)
    return (resp['SecretString'], resp['SecretBinary'])


def set_value(client: any, name: str, data: any, is_binary: bool) -> tuple:
    if is_binary:
        resp = client.put_secret_value(SecretId=name, SecretBinary=data)
        return (resp['Name'], resp['ARN'])

    else:
        resp = client.put_secret_value(SecretId=name, SecretString=data)
        return (resp['Name'], resp['ARN'])


try:
    client = boto3.client('secretsmanager')
    for name in secrets:
        is_binary = secrets[name]['Binary']
        file_data = read_file(secrets[name]['File'], is_binary)

        if not describe_secret(client, name):
            resp = create_secret(client, name, file_data, is_binary)
            print('Create: {} ({})'.format(*resp))

        else:
            resp = set_value(client, name, file_data, is_binary)
            print('Update: {} ({})'.format(*resp))


except Exception:
    traceback.print_exc()
    sys.exit(1)
