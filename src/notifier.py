import os
import json
import boto3


sns = boto3.client('sns')
TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def send_notification(event, context):
    for record in event.get('Records', []):
        if record.get('eventName') == 'INSERT':
            new = record['dynamodb'].get('NewImage', {})
            order_id = new.get('orderId', {}).get('S')
            created = new.get('createdAt', {}).get('S')


            msg = {
            'orderId': order_id,'createdAt': created,'message': 'New order created'
}
            sns.publish(TopicArn=TOPIC_ARN, Message=json.dumps(msg), Subject='New Order')


    return {'statusCode': 200}