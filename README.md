# Log Rotation

Rotate Lambda daily log from CloudWatch to S3.

## How to Use

Deploy to AWS Lambda with Serverless:

```bash
serverless deploy --stage production
```

## Create Stack

```bash
serverless create --template aws-python3 --path log-rotation
```

## Delete Stack

To delete the whole stack:

```bash
serverless remove --stage production --region us-east-1
```
