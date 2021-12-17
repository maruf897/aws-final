import json
import boto3
import os

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_POOL_ID = os.environ.get("USER_POOL_CLIENT_ID")


def SignUp_handler(event, context):

    username = event['body']
    data = json.loads(username)
    email = data["email"]
    password = data["password"]

    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId=CLIENT_POOL_ID,

        Username=email,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
        ],
        ValidationData=[
            {
                'Name': 'email',
                'Value': email
            },
        ],
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
            # "response": response
            # "location": ip.text.replace("\n", "")
        }),
    }
