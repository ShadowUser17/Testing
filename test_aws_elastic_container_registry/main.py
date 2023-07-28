import traceback
import base64
import boto3

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

def get_auth_token(client: any) -> list:
    '''
    return ["user", "password"]
    '''
    responce = client.get_authorization_token()
    tmp = base64.b64decode(responce["authorizationData"][0]["authorizationToken"])
    return tmp.decode().split(":")


def describe_repos(client: any, repo_list: list) -> list:
    responce = client.describe_repositories(repositoryNames=repo_list)
    return responce["repositories"]


def list_repos(client: any, items: int = 100) -> list:
    responce = client.describe_repositories(maxResults=items)
    return responce["repositories"]


def get_repo_tags(client: any, arn: str) -> list:
    responce = client.list_tags_for_resource(resourceArn=arn)
    return responce["tags"]


try:
    client = boto3.client("ecr")
    print(get_auth_token(client))

except Exception:
    traceback.print_exc()
