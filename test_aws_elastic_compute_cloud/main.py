import traceback
import boto3

# AWS_DEFAULT_REGION
# AWS_PROFILE
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

def list_instances(client: any, items: int = 100) -> list:
    response = client.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ],
        MaxResults=items
    )
    return response["Reservations"]


def describe_instance(client: any, instance_id: str) -> dict:
    response = client.describe_instances(InstanceIds=[instance_id])
    return response["Reservations"][0]["Instances"][0]


try:
    client = boto3.client("ec2")
    for group in list_instances(client):
        print(group["Groups"])

        for instance in group["Instances"]:
            print("{}:".format(instance["InstanceId"]))

            for tag in instance["Tags"]:
                print("\t{}: {}".format(tag["Key"], tag["Value"]))

except Exception:
    traceback.print_exc()
