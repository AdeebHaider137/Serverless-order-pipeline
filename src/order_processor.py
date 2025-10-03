import json
import os
import boto3
import time
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE')

def process_order(event, context):
    table = dynamodb.Table(TABLE_NAME)
    records = event.get('Records', [])
    successes = 0

    for r in records:
        body = r.get('body')
        try:
            order = json.loads(body)
            order_id = order.get('orderId') or f"ord_{int(time.time()*1000)}"
            now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            item = {
                'orderId': order_id,
                'createdAt': now,
                'status': 'PENDING',
                'items': order.get('items', []),
                'totalAmount': order.get('totalAmount', 0),
                'customerId': order.get('customerId')
            }

            table.put_item(Item=item)
            successes += 1
        except ClientError as e:
            print('DynamoDB ClientError', e)
            raise
        except Exception as e:
            print('Failed to process record', e, 'body:', body)
            raise

    return { 'statusCode': 200, 'processed': successes }
