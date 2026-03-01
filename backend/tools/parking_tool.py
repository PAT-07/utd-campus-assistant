import boto3
import json
import os

# s3 = boto3.client("s3")
# BUCKET = os.getenv("DATA_BUCKET", "awsclub-data")

# ---- Temporary sample data ----
sample_parking_data = [
    {"lot": "PS1", "type": "green", "availability": "high"},
    {"lot": "Lot J", "type": "orange", "availability": "medium"},
    {"lot": "PS3", "type": "gold", "availability": "low"},
    {"lot": "Lot H", "type": "purple", "availability": "high"},
]

def lambda_handler(event, context):
    args = event.get("tool_args", {})
    permit = (args.get("permit") or "").lower()

    # ---- S3 disabled ----
    # obj = s3.get_object(Bucket=BUCKET, Key="parking.json")
    # data = json.loads(obj["Body"].read())

    data = sample_parking_data

    if permit:
        filtered = [p for p in data if p["type"].lower() == permit]
    else:
        filtered = data

    return {
        "statusCode": 200,
        "results": filtered
    }