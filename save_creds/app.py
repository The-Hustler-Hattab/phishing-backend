import json
import boto3
import datetime
import uuid

DYNAMO_DB_CLIENT = boto3.client('dynamodb')

TABLE_NAME="saveCreds"

HEADERS = {
        'Access-Control-Allow-Origin': '*'

    }


def getCurrentTime():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")



def lambda_handler(event, context):

# parse request body
    body = json.loads(event["body"])
    username= body["username"]
    password= body["password"]
    site= body["site"]

    
    item = {
    'USERNAME': {"S":username},            
    'PASSWORD': {"S":password},
    'SITE'    : {"S":site},
    'TIME': {"S":getCurrentTime()},
    'id': {"S": str(uuid.uuid4()) },
    
    }
    
    response = DYNAMO_DB_CLIENT.put_item(
    TableName=TABLE_NAME,  # Replace with your table name
    Item=item
    )

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({
            "message": "creds were saved successfuly",
            "DynamoDbResponse": response
        }),
    }
