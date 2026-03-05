import json
import boto3
import os
import re

# ---------------------------------------------------------------------------
# User-editable configuration
# ---------------------------------------------------------------------------
# AWS region where Lambda, Bedrock model access, and KB are available.
REGION = os.environ.get("AWS_REGION", "us-east-2")

# Bedrock Knowledge Base ID from the AWS console.
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID")

# Gemma 3 4B model ARN (foundation model, no inference profile needed)
MODEL_ID = os.environ.get("MODEL_ID", "google.gemma-3-4b-it")
MODEL_ARN = f"arn:aws:bedrock:{REGION}::foundation-model/{MODEL_ID}"
# MODEL_ARN = "arn:aws:bedrock:us-east-2:150278104193:inference-profile/global.anthropic.claude-opus-4-6-v1"

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

                    Use ONLY the retrieved information below to answer the user's question.

                    Retrieved Information:
                    $search_results$

                    User Question:
                    $query$

                    If answer is not available, say: "I do not have that information in my knowledge base."
                    """

# Initialize Bedrock agent
bedrock_agent = boto3.client(service_name="bedrock-agent-runtime", region_name=REGION)


def parse_dining(text):
    """
    Parse the raw text from Gemma into structured JSON
    Expected format:
    The Market   (Naveen Jindal School of Management (JSOM)): 10:00 a.m. - 3:00 p.m.
    """
    results = []
    # Split lines
    lines = text.split("\n")
    for line in lines:
        match = re.match(r"^(.*?)\s+\((.*?)\):\s+(.*)$", line.strip())
        if match:
            name, location, timings = match.groups()
            results.append(
                {
                    "name": name.strip(),
                    "location": location.strip(),
                    "timings": timings.strip(),
                }
            )
    return results


def lambda_handler(event, context):
    try:
        body = event.get("body", "{}")
        user_message = body.get("message")
        if not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'message' in request body"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            }

        orchestrationConfiguration = {
            "promptTemplate": {"textPromptTemplate": ORCHESTRATION_PROMPT}
        }

        generationConfiguration = {
            "promptTemplate": {"textPromptTemplate": GENERATION_PROMPT},
            "inferenceConfig": {
                "textInferenceConfig": {
                    "maxTokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                }
            },
        }

        response = bedrock_agent.retrieve_and_generate(
            input={"text": user_message},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                    "orchestrationConfiguration": orchestrationConfiguration,
                    "generationConfiguration": generationConfiguration,
                },
            },
        )

        raw_text = response["output"]["text"]
        # Try to parse as dining, fallback to raw text
        if (
            DINING_PARSE_KEYWORD_1 in user_message.lower()
            and DINING_PARSE_KEYWORD_2 in user_message.lower()
        ):
            parsed = parse_dining(raw_text)
        else:
            parsed = [{"text": raw_text}]  # fallback for events/parking

        return {
            "statusCode": 200,
            "body": {"raw_response": raw_text, "parsed_response": parsed},
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": ALLOW_ORIGIN,
            },
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": ALLOW_ORIGIN,
            },
        }


# import json
# import boto3
# import os


# REGION = os.environ.get("AWS_REGION", "us-east-2")
# KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID")

# # Claude model ARN in Bedrock
# MODEL_ARN = "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-sonnet-4-6"

# # Initialize Bedrock client
# bedrock_agent = boto3.client(
#     service_name="bedrock-agent-runtime",
#     region_name=REGION
# )

# def lambda_handler(event, context):
#     try:
#         body = event.get("body", "{}")
#         user_message = body.get("message")

#         if not user_message:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "Missing 'message' in request body"}),
#                 "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
#             }

#         # Generation prompt instructing Claude to return JSON
#         generation_prompt = f"""
# You are the UTD Campus Assistant.

# Use ONLY the retrieved information below to answer the user's question.

# Retrieved Information:
# $search_results$

# User Question:
# {user_message}

# Return the answer in JSON format with the following structure:

# - For dining questions:
# [
#   {{
#     "name": "<name of the dining place>",
#     "location": "<building/location>",
#     "timings": "<hours of operation>"
#   }}
# ]

# - For events questions:
# [
#   {{
#     "event_name": "<event name>",
#     "building": "<building>",
#     "room": "<room>",
#     "duration": "<duration in minutes>"
#   }}
# ]

# - For parking questions:
# [
#   {{
#     "garage": "<garage/lot name>",
#     "level": "<level if applicable>",
#     "permit_type": "<permit type or info>"
#   }}
# ]

# If there is no relevant information, return an empty array.
# """

#         # Call Bedrock RetrieveAndGenerate
#         response = bedrock_agent.retrieve_and_generate(
#             input={"text": user_message},
#             retrieveAndGenerateConfiguration={
#                 "type": "KNOWLEDGE_BASE",
#                 "knowledgeBaseConfiguration": {
#                     "knowledgeBaseId": KNOWLEDGE_BASE_ID,
#                     "modelArn": MODEL_ARN,
#                     "generationConfiguration": {
#                         "promptTemplate": {"textPromptTemplate": generation_prompt},
#                         "inferenceConfig": {"textInferenceConfig": {"maxTokens": 400, "temperature": 0.2}}
#                     }
#                 }
#             }
#         )

#         raw_text = response["output"]["text"]

#         try:
#             parsed_response = json.loads(raw_text)
#         except Exception:
#             parsed_response = []

#         return {
#             "statusCode": 200,
#             "body": {
#                 "raw_response": raw_text,
#                 "parsed_response": parsed_response
#             },
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
#         }

#     except Exception as e:
#         return {
#             "statusCode": 500,
#             "body": json.dumps({"error": str(e)}),
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
#         }
