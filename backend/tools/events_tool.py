import boto3, json, os

# s3 = boto3.client("s3")
# BUCKET = os.getenv("DATA_BUCKET", "awsclub-data")

# ---- Temporary sample data ----
sample_events_data = [
    {"title": "HackUTD", "category": "tech", "location": "SSA"},
    {"title": "Career Expo", "category": "career", "location": "VFAC"},
    {"title": "Diwali Night", "category": "cultural", "location": "SU"},
    {"title": "Coding Workshop", "category": "tech", "location": "ECSS"},
]

def lambda_handler(event, context):
    args = event.get("tool_args", {})
    category = (args.get("category") or "").lower()

    # ---- S3 disabled ----
    # obj = s3.get_object(Bucket=BUCKET, Key="events.json")
    # data = json.loads(obj["Body"].read())

    data = sample_events_data

    if category:
        filtered = [e for e in data if e["category"].lower() == category]
    else:
        filtered = data

    return {
        "statusCode": 200,
        "results": filtered
    }