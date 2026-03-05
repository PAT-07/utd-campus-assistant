import json
import os
import re

import boto3

# ---------------------------------------------------------------------------
# User-editable configuration
# ---------------------------------------------------------------------------
# AWS region where Lambda, Bedrock model access, and KB are available.
REGION = os.environ.get("AWS_REGION", "us-east-1")

# Bedrock Knowledge Base ID from the AWS console.
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")

# Foundation model ARN for Gemma.
MODEL_ID = os.environ.get("MODEL_ID", "google.gemma-3-4b-it")
MODEL_ARN = f"arn:aws:bedrock:{REGION}::foundation-model/{MODEL_ID}"

# Inference controls (safe to tune).
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "300"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.2"))

# CORS setting for browser frontend.
ALLOW_ORIGIN = os.environ.get("ALLOW_ORIGIN", "*")

# Optional keywords used for dining parsing rule.
DINING_PARSE_KEYWORD_1 = os.environ.get("DINING_PARSE_KEYWORD_1", "open").lower()
DINING_PARSE_KEYWORD_2 = os.environ.get("DINING_PARSE_KEYWORD_2", "dining").lower()

# Prompt templates used by RetrieveAndGenerate.
ORCHESTRATION_PROMPT = """
    You are orchestrating retrieval for the UTD Campus Assistant.
    Conversation History:
    $conversation_history$

    Instructions for generation:
    $output_format_instructions$

    User Question:
    $query$
"""

GENERATION_PROMPT = """
    You are the UTD Campus Assistant.
    Use ONLY the retrieved information below to answer.

    Retrieved Information:
    $search_results$

    User Question:
    $query$

    If answer is not available, say:
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


def parse_dining(text):
    """
    Parse lines like:
    The Market (Naveen Jindal School of Management): 10:00 a.m. - 3:00 p.m.
    """
    items = []
    for line in text.split("\n"):
        match = re.match(r"^(.*?)\s+\((.*?)\):\s+(.*)$", line.strip())
        if match:
            name, location, timings = match.groups()
            items.append(
                {
                    "name": name.strip(),
                    "location": location.strip(),
                    "timings": timings.strip(),
                }
            )
    return items


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

        orchestration_configuration = {
            "promptTemplate": {"textPromptTemplate": ORCHESTRATION_PROMPT}
        }

        generation_configuration = {
            "promptTemplate": {"textPromptTemplate": GENERATION_PROMPT},
            "inferenceConfig": {
                "textInferenceConfig": {
                    "maxTokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                }
            },
        }

        rag_response = bedrock_agent.retrieve_and_generate(
            input={"text": user_message},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                    "orchestrationConfiguration": orchestration_configuration,
                    "generationConfiguration": generation_configuration,
                },
            },
        )

        raw_text = rag_response["output"]["text"]
        if (
            DINING_PARSE_KEYWORD_1 in user_message.lower()
            and DINING_PARSE_KEYWORD_2 in user_message.lower()
        ):
            parsed = parse_dining(raw_text)
        else:
            parsed = [{"text": raw_text}]

        return _response(200, {"raw_response": raw_text, "parsed_response": parsed})
    except Exception as exc:
        return _response(500, {"error": str(exc)})
