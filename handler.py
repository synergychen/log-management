import boto3
import datetime
import json
import os
import re
import time

def query(log_group, start_time, end_time):
    client = boto3.client('logs')

    # CloudWatch log query
    query = 'fields @timestamp, @message | filter ispresent(appName)'
    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )

    # Polling query results
    query_id = start_query_response['queryId']
    response = None
    print('Quering ...')
    while response == None or response['status'] == 'Running':
        time.sleep(0.3)
        response = client.get_query_results(
            queryId=query_id
        )
    print('Query completed.')
    return response

def parse_results(data):
    res = { 'data': [] }
    for logs in data['results']:
        matched = list(filter(lambda log: log['field'] == '@message', logs))
        if len(matched) > 0:
            m = re.search('{.*}$', matched[0]['value'])
            if m is not None:
                json_data = json.loads(m.group(0))
                res['data'].append(json_data)
    return res

def timestamps(retention_days=1):
    curt = datetime.datetime.now()
    prev = curt - datetime.timedelta(retention_days)
    curt_timestamp = int(curt.date().strftime('%s'))
    prev_timestamp = int(prev.date().strftime('%s'))
    curt_date = curt.date().strftime('%Y%m%d')
    prev_date = prev.date().strftime('%Y%m%d')
    return {
        'start_time': prev_timestamp,
        'start_year': str(prev.year),
        'start_month': str(prev.month).zfill(2),
        'start_date': prev_date,
        'end_time': curt_timestamp,
        'end_year': str(curt.year),
        'end_month': str(curt.month).zfill(2),
        'end_date': curt_date
    }

def save_to_s3(bucket_name, prefix, data):
    s3 = boto3.resource('s3')
    print('Saving to S3 ...')
    s3.Object(bucket_name, prefix).put(Body=data)
    print('Saved successfully.')

def handler(event, context):
    # Settings
    retention_days = int(os.environ.get("RETENTION_DAYS"))
    bucket_name = os.environ.get("S3_LOG_BUCKET")
    parent_folder = 'lambda-logs'
    log_groups = os.environ.get("CLOUDWATCH_LOGS").split(",")

    # Calculations
    date_and_time = timestamps(retention_days)
    start_time = date_and_time['start_time']
    end_time = date_and_time['end_time']
    end_year = date_and_time['end_year']
    end_month = date_and_time['end_month']
    end_date = date_and_time['end_date']

    for log_group in log_groups:
        print('Rotating logs for: ' + log_group + ' ...')
        # Query log
        results = query(log_group, start_time, end_time)

        # Parse results
        json_data = parse_results(results)

        # Save to S3
        prefix = parent_folder + '/' + log_group.split('/')[-1] + '/' + end_year + '/' + end_month + '/' + end_date + '.json'
        data = json.dumps(json_data, ensure_ascii=False)
        save_to_s3(bucket_name, prefix, data)

if __name__ == '__main__':
    handler()
