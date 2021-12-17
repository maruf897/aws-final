import json
import boto3
import os
import datetime


ct = datetime.datetime.now()

TABLE_NAME = os.environ.get("TABLE_NAME")


def get_Category_list(event, context):
    clientdb = boto3.client('dynamodb')

    categ = clientdb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='pk = :pkval',
        ExpressionAttributeValues={":pkval": {'S': "Categ#"}}
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": categ,
            # "location": ip.text.replace("\n", "")
        }),
    }


def add_Category(event, context):
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
    categname = data["categorName"]
    clientdb.put_item(
        TableName=TABLE_NAME,
        Item={
            'pk': {'S': 'Categ#'},
            'sk': {'S': categname}
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Category uploaded",
            # "location": ip.text.replace("\n", "")
        }),
    }
