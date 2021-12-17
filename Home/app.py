import json
import boto3
import os
import datetime


ct = datetime.datetime.now()

TABLE_NAME = os.environ.get("TABLE_NAME")


def get_jokes(event, context):

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
    clientdb = boto3.client('dynamodb')
    responsedb = clientdb.get_item(
        TableName=TABLE_NAME,
        Key={
            'pk': {"S": 'User#'},
            'sk': {"S": user},
        })
    joke_list = []
    try:
        user_data = responsedb['Item']['interest']["SS"]
        if user_data is not None:
            for interest in user_data:
                jokes = clientdb.query(
                    TableName=TABLE_NAME,
                    KeyConditionExpression='pk = :pkval AND begins_with ( sk , :skval )',
                    ExpressionAttributeValues={":pkval": {'S': "Joke#"},
                                               ":skval": {'S': interest}
                                               }
                )
                joke_list.append(jokes)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": joke_list,
                    # "location": ip.text.replace("\n", "")
                }),
            }
    except:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "update profile",
                # "location": ip.text.replace("\n", "")
            }),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "no jokes",
            # "location": ip.text.replace("\n", "")
        }),
    }


def post_joke(event, context):
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
    joke_category = data["joke_category"]
    joke = data["joke"]

    clientdb = boto3.client('dynamodb')
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'JokeReq#'},
            'sk': {'S': user + str(ct)},
            'joke': {"S": joke},
            'joke_categ': {"S": joke_category}
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Joke In review",
            # "location": ip.text.replace("\n", "")
        }),
    }
