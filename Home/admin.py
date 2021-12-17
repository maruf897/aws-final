import json
import boto3
import os
import datetime


ct = datetime.datetime.now()

TABLE_NAME = os.environ.get("TABLE_NAME")


def get_jokeReq_list(event, context):
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
            'pk': {"S": 'AdminReq#'},
            'sk': {"S": user},
        })
    admin_stat = responsedb['Item']['status']["S"]
    if(admin_stat != "true"):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Unauthorized",
                # "location": ip.text.replace("\n", "")
            }),
        }

    jokes = clientdb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='pk = :pkval',
        ExpressionAttributeValues={":pkval": {'S': "JokeReq#"}}
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": jokes,
            # "location": ip.text.replace("\n", "")
        }),
    }


def accept_jokeReq(event, context):
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
            'pk': {"S": 'AdminReq#'},
            'sk': {"S": user},
        })
    admin_stat = responsedb['Item']['status']["S"]
    if(admin_stat != "true"):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Unauthorized",
                # "location": ip.text.replace("\n", "")
            }),
        }
    body = event['body']
    data = json.loads(body)
    sk = data["sk"]
    pk = data["pk"]

    joke = clientdb.get_item(
        TableName=TABLE_NAME,
        Key={
            'pk': {"S": pk},
            'sk': {"S": sk},
        })
    joke_val = joke['Item']['joke']["S"]
    joke_cat = joke['Item']['joke_categ']["S"]
    metadata = joke['Item']['sk']["S"]
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'Joke#'},
            'sk': {'S': joke_cat + str(ct)},
            'joke': {"S": joke_val},
            'owner': {"S": metadata}
        })
    clientdb.delete_item(
        TableName=TABLE_NAME,
        Key={
            'pk': {"S": pk},
            'sk': {"S": sk},
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Joke accepted",
            # "location": ip.text.replace("\n", "")
        }),
    }
