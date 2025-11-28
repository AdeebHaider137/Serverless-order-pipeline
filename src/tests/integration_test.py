import json
import boto3
import os


sqs = boto3.client("sqs")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")


QUEUE_URL = os.environ.get("ORDERS_QUEUE_URL")
TABLE_NAME = os.environ.get("ORDERS_TABLE")




def load_sample_orders():
    with open(os.path.join(os.path.dirname(__file__), "sample_orders.json")) as f:
        return json.load(f)




def send_orders_to_sqs(orders):
    for order in orders:
        resp = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(order))
        print("Sent order:", order["orderId"], "MessageId:", resp["MessageId"])




def verify_orders_in_dynamodb(orders):
    table = dynamodb.Table(TABLE_NAME)
    for order in orders:
        resp = table.get_item(Key={"orderId": order["orderId"]})
        if "Item" in resp:
            print("Order found in DynamoDB:", resp["Item"])
        else:
            print("Order not found:", order["orderId"])




def run_integration_test():
    print("\n--- Running Integration Test ---\n")
    orders = load_sample_orders()
    send_orders_to_sqs(orders)
    print("Waiting for processing...")
    import time; time.sleep(10)
    verify_orders_in_dynamodb(orders)
    print("\n--- Test Completed ---\n")




if __name__ == "__main__":
    run_integration_test()
