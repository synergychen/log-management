import os
import json

def collect(event, context):
    print(event['body'])
    return {
        'statusCode': 200,
        'body': 'OK',
        'headers': {
            'Content-Type': 'application/json'
        }
    }
