import json
import boto3


DYNAMO_DB_CLIENT = boto3.client('dynamodb')

TABLE_NAME="saveCreds"
HEADERS = {
        'Access-Control-Allow-Origin': '*',
        "Content-Type": "application/json" 

    }

RESPONSE = {
        "statusCode": 400,
        "headers": HEADERS,
        "body": json.dumps( { "error":"Something wrong happend" })         # Convert Python dictionary to JSON string
    }

#----------------------- get endpoint functions
def scan_dynamodb_table():
    records = []
    response = DYNAMO_DB_CLIENT.scan(TableName=TABLE_NAME)
    records.extend(response.get('Items', []))

    while 'LastEvaluatedKey' in response:
        response = DYNAMO_DB_CLIENT.scan(
            TableName=TABLE_NAME,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        records.extend(response.get('Items', []))

    return records
def manpulateRecordsToDesiredJsonFormat(json):
    for row in json:
        for key , value in row.items():
            row[key]= value["S"]
    return json
def getAllCredsRequestHandler():
    response_body = RESPONSE;
    response_body['statusCode']=200
    response_body['body'] = json.dumps( {
        'message': 'Records Retrived Successfuly',
        'dynamoDbRecords':manpulateRecordsToDesiredJsonFormat(scan_dynamodb_table()) }  )
    return response_body
#----------------------- get endpoint functions END

#----------------------- POST endpoint functions
def deleteByIdDynamoDb(id):
    key = {
    'id': {'S': id}
    }
    try:
        response = DYNAMO_DB_CLIENT.delete_item(
            TableName=TABLE_NAME,
            Key=key
        )
        return "Item deleted successfully."
    except Exception as e:
        return f"Error deleting item: {str(e)}"    

def deleteCredRequestHandler(event):
    body = json.loads(event["body"])
    itemId= body["id"]    
    
    response_body = RESPONSE;
    response_body['statusCode']=200
    response_body['body']=json.dumps( { "message": deleteByIdDynamoDb(itemId)
        
    } )
    return response_body
#----------------------- POST endpoint functions END




def lambda_handler(event, context):
    print(event)

    if event['httpMethod']=='GET':
        return getAllCredsRequestHandler()
        
    if event['httpMethod']=='POST':
        return deleteCredRequestHandler(event)
    
    return RESPONSE
