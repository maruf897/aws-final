import json
import boto3
import os

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_POOL_ID = os.environ.get("USER_POOL_CLIENT_ID")


def SignIn_handler(event, context):

    body = event['body']
    data = json.loads(body)
    email = data["username"]
    password = data["password"]

    
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password},
            ClientId=CLIENT_POOL_ID
            )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
            # "response": response
            # "location": ip.text.replace("\n", "")
        }),
    }
