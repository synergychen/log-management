# Log Rotation

Filter, parse CloudWatch logs and upload to S3.

## Why

CloudWatch logs are noisy sometimes and could be hard to query and aggregate across different systems. This lambda function provide a way to filter, parse CloudWatch logs (from different log groups) and upload results to S3 for further analysis.

## How to Use

### 1. Create a `secrets.json` file

```json
{
  "S3_LOG_BUCKET": "<s3 bucket name>",
  "RETENTION_DAYS": 1,
  "CLOUDWATCH_LOGS": "<logs separated by comma>"
}
```

### 2. Deploy

Deploy to AWS Lambda with Serverless:

```bash
serverless deploy --stage production
```

## Test

To test locally:

```bash
serverless invoke local --function perform
```

## Others

### Create from scratch

```bash
serverless create --template aws-python3 --path log-rotation
```

### Delete service

To delete the whole stack:

```bash
serverless remove --stage production --region us-east-1
```
