import os
import json
import boto3

sns = boto3.client('sns')
TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

if not TOPIC_ARN:
    raise ValueError("SNS_TOPIC_ARN environment variable is not set")

def send_notification(event, context):
    for record in event.get('Records', []):
        if record.get('eventName') == 'INSERT':
            new = record['dynamodb'].get('NewImage', {})
            order_id = new.get('orderId', {}).get('S', 'unknown')
            created = new.get('createdAt', {}).get('S', 'unknown')

            msg = {
                'orderId': order_id,
                'createdAt': created,
                'message': 'New order created'
            }

            print(f"[INFO] Publishing notification for order {order_id}")
            try:
                sns.publish(TopicArn=TOPIC_ARN, Message=json.dumps(msg), Subject='New Order')
            except Exception as e:
                print(f"[ERROR] Failed to publish notification for order {order_id}: {e}")

    return {'statusCode': 200}
