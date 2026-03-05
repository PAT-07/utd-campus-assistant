import json
import os

import boto3

# ---------------------------------------------------------------------------
# User-editable configuration
# ---------------------------------------------------------------------------
# AWS region where Lambda, Bedrock model access, and KB are available.
REGION = os.environ.get("AWS_REGION", "us-east-1")

# Bedrock Knowledge Base ID from the AWS console.
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")

# Recommended: use an inference profile ARN for Claude in Bedrock.
# Example:
# arn:aws:bedrock:us-east-1:<account-id>:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0
MODEL_ARN = os.environ.get("MODEL_ARN", "")

# Inference controls (safe to tune).
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "400"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.2"))

# CORS setting for browser frontend.
ALLOW_ORIGIN = os.environ.get("ALLOW_ORIGIN", "*")

# Prompt template used for response generation.
GENERATION_PROMPT = """
    You are the UTD Campus Assistant.

    Use ONLY the retrieved knowledge-base content to answer.
    If the answer is unavailable in the retrieved context, say:
    "I do not have that information in my knowledge base."
"""

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name=REGION)


def _parse_event_body(event):
    body = event.get("body", {})
    if isinstance(body, str):
        body = json.loads(body or "{}")
    return body


def _response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": ALLOW_ORIGIN,
        },
        "body": json.dumps(payload),
    }


def lambda_handler(event, context):
    try:
        body = _parse_event_body(event)
        user_message = body.get("message")

        if not user_message:
            return _response(400, {"error": "Missing 'message' in request body"})
        if not KNOWLEDGE_BASE_ID:
            return _response(
                500, {"error": "Missing KNOWLEDGE_BASE_ID environment variable"}
            )
        if not MODEL_ARN:
            return _response(500, {"error": "Missing MODEL_ARN environment variable"})

        rag_response = bedrock_agent.retrieve_and_generate(
            input={"text": user_message},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                    "generationConfiguration": {
                        "promptTemplate": {"textPromptTemplate": GENERATION_PROMPT},
                        "inferenceConfig": {
                            "textInferenceConfig": {
                                "maxTokens": MAX_TOKENS,
                                "temperature": TEMPERATURE,
                            }
                        },
                    },
                },
            },
        )

        answer = rag_response["output"]["text"]
        return _response(
            200, {"raw_response": answer, "parsed_response": [{"text": answer}]}
        )
    except Exception as exc:
        return _response(500, {"error": str(exc)})
