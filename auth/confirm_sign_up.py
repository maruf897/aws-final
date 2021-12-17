import json
import boto3
import os

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_POOL_ID = os.environ.get("USER_POOL_CLIENT_ID")
TABLE_NAME = os.environ.get("TABLE_NAME")


def ConfirmSingUp_handler(event, context):

    body = event['body']
    data = json.loads(body)
    email = data["username"]
    password = data["code"]

    client = boto3.client('cognito-idp')
    response = client.confirm_sign_up(
        ClientId=CLIENT_POOL_ID,
        Username=email,
        ConfirmationCode=password

    )

    clientdb = boto3.client('dynamodb')
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'User#'},
            'sk': {'S': email}
        })
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'AdminReq#'},
            'sk': {'S': email},
            'status': {"S": "false"}
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
            # "response": response
            # "location": ip.text.replace("\n", "")
        }),
    }
