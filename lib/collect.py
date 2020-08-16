import os
import json

def collect(event, context):
    if not verify_token(event):
        response ={
            'statusCode': 401,
            'body': 'Invalid Token',
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        print(response)
        return response

    print(json.loads(event['body']))
    return {
        'statusCode': 200,
        'body': 'OK',
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def verify_token(event):
    authorization_token = event.get('headers', {}).get('Authorization')
    return authorization_token == 'Basic ' + os.environ.get("AUTH_TOKEN")
