import json
import boto3
import os
import datetime


ct = datetime.datetime.now()

TABLE_NAME = os.environ.get("TABLE_NAME")


def update_profile(event, context):
    headers = event['headers']
    token = headers['AC']
    client = boto3.client('cognito-idp')
    try:
        response = client.get_user(
            AccessToken=token
        )
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "login again",
            }),
        }

    user = response['Username']
    body = event['body']
    data = json.loads(body)
    interests = data["interests"]

    clientdb = boto3.client('dynamodb')
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'User#'},
            'sk': {'S': user},
            'interest': {"SS": interests}
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Profile Updated",
            # "location": ip.text.replace("\n", "")
        }),
    }
