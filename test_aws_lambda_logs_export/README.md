#### Deploy:
- Create IAM policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AccessToLogs",
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AccessToVPC",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:AttachNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:CreateTags"
            ],
            "Resource": "*"
        }
    ]
}
```
- Create IAM role for Lambda.
- Create Lambda (python3).
- Configure environment variable: `LOKI_ENDPOINT`
- Attach VPC and configure access to Loki ingress.
- Create in CloudWatch Logs subscription filter for log groups.

#### Testing:
```bash
python3 -m venv --upgrade-deps env && \
./env/bin/pip3 install -r requirements.txt
```
```bash
./env/bin/python3 ./testing.py
```
