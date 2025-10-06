import json
import os
import boto3
import time
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE")
table = dynamodb.Table(TABLE_NAME)

def process_order(event, context):
    records = event.get("Records", [])
    successes, duplicates, failures = 0, 0, 0

    for r in records:
        body = r.get("body")
        if not body:
            print("[WARN] Empty record body, skipping.")
            continue

        try:
            order = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in body: {e}")
            failures += 1
            continue

        # Ensure stable and unique orderId
        order_id = order.get("orderId") or f"ord_{int(time.time() * 1000)}"

        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        raw_total = order.get("totalAmount", 0)
        total_cents = int(round(float(raw_total) * 100))

        item = {
            "orderId": order_id,
            "createdAt": now,
            "status": "PENDING",
            "items": order.get("items", []),
            "totalAmount": total_cents,
            "customerId": order.get("customerId"),
        }

        try:
            #Conditional write to ensure idempotency
            table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(orderId)"
            )
            print(f"[SUCCESS] Inserted order {order_id}")
            successes += 1

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                # Duplicate order already exists in DynamoDB
                print(f"[DUPLICATE] Order {order_id} already exists, skipping duplicate insert.")
                duplicates += 1
                continue
            else:
                print(f"[ERROR] DynamoDB ClientError: {error_code} - {e}")
                failures += 1
                raise  # rethrow to let Lambda handle DLQ

        except Exception as e:
            print(f"[ERROR] Unexpected failure for order {order_id}: {e}")
            failures += 1
            raise

    result = {
        "statusCode": 200,
        "processed": successes,
        "duplicates": duplicates,
        "failures": failures
    }

    print("[SUMMARY]", json.dumps(result))
    return result