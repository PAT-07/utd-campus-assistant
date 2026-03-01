import boto3
import json
import os

# s3 = boto3.client("s3")
# BUCKET = os.getenv("DATA_BUCKET", "awsclub-data")

# ---- Temporary sample data ----
sample_dining_data = [
    {"name": "Panda Express", "tags": ["asian", "veg options"]},
    {"name": "Chick-fil-A", "tags": ["fast food", "chicken"]},
    {"name": "Halal Shack", "tags": ["halal", "mediterranean"]},
    {"name": "Saffron Diner", "tags": ["indian", "vegan"]},
    {"name": "Moe's Southwest Grill", "tags": ["mexican", "veg options"]},
]

def lambda_handler(event, context):
    args = event.get("tool_args", {})
    diet = args.get("diet", "").lower()

    # ---- S3 disabled ----
    # obj = s3.get_object(Bucket=BUCKET, Key="dining.json")
    # data = json.loads(obj["Body"].read())

    data = sample_dining_data

    if diet:
        filtered = [
            r for r in data
            if diet in [t.lower() for t in r.get("tags", [])]
        ]
    else:
        filtered = data

    return {
        "statusCode": 200,
        "results": filtered
    }
