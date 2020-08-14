# Log Management

Log management provides easy APIs to collect, filter, parse and save logs.

The service is based on Lambda, which inclues:

- A service to collect logs, similar to Splunk HEC (HTTP Event Collector).
- A service to filter, parse CloudWatch logs and upload to S3.

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
serverless create --template aws-python3 --path log-management
```

### Delete service

To delete the whole stack:

```bash
serverless remove --stage production --region us-east-1
```
