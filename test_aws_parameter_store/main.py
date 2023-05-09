import sys
import boto3
import base64
import pathlib
import traceback

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

ssm_params = {
    "/configs/testing/cert"    : {"secure": True,  "file": True,  "value": "app/cert.pem"},
    "/configs/testing/cert_key": {"secure": True,  "file": True,  "value": "app/cert.key"},
    "/configs/testing/env"     : {"secure": False, "file": False, "value": "testing"},
    "/configs/testing/app_conf": {"secure": False, "file": True,  "value": "app/config.json"}
}


def get_string_param(param_name: str, secure: bool) -> str:
    response = client.get_parameter(
        Name=param_name,
        WithDecryption=secure
    )

    return response['Parameter']['Value']


def get_file_param(param_name: str, file_name: str, secure: bool) -> None:
    file = pathlib.Path(file_name)
    data = base64.b64decode(get_string_param(param_name, secure))
    file.write_bytes(data)


def put_string_param(param_name: str, param_value: str, secure: bool) -> None:
    client.put_parameter(
        Name=param_name,
        Value=param_value,
        Type='SecureString' if secure else 'String',
        Tier='Standard',
        Overwrite=True
    )


def put_file_param(param_name: str, file_name: str, secure: bool) -> None:
    file = pathlib.Path(file_name)
    data = base64.b64encode(file.read_bytes())
    put_string_param(param_name, data.decode(), secure)


try:
    client = boto3.client('ssm')

    for (param_name, param_item) in ssm_params.items():
        print("Store:", param_name)

        if param_item['file']:
            put_file_param(param_name, param_item['value'], param_item['secure'])

        else:
            put_string_param(param_name, param_item['value'], param_item['secure'])

except Exception:
    traceback.print_exc()
    sys.exit(1)
