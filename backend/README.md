# Backend (Lambda + API Gateway + Bedrock KB)

This backend powers the UTD chatbot API.

## What is in this folder

- `chat-handler/lambda_handler.py`: your current handler file.
- `chat-handler/lambda_handler_claude.py`: handler configured for Claude via Bedrock inference profile.
- `chat-handler/lambda_handler_gemma.py`: handler configured for Gemma foundation model.

## Architecture

1. Frontend sends `POST /askutd` with `{ "message": "..." }`.
2. API Gateway triggers Lambda.
3. Lambda calls Bedrock `RetrieveAndGenerate` with your Knowledge Base ID.
4. Bedrock retrieves data from S3-backed KB and generates final answer.
5. Lambda returns JSON to frontend.

---

## AWS setup (common for both models)

1. Create or choose an S3 bucket for data files.
2. Upload data JSON files (`dining.json`, `events.json`, `parking.json`).
3. In Bedrock console:
   1. Open `Knowledge bases`.
   2. Create a knowledge base.
   3. Set S3 as data source and sync.
   4. Copy the `Knowledge Base ID`.
4. Create Lambda function (Python 3.12 or 3.11).
5. Add IAM permissions to Lambda role:
   - `bedrock:RetrieveAndGenerate`
   - S3 read permissions for KB data source bucket (if needed by your setup)
   - CloudWatch Logs permissions
6. Configure API Gateway route (for example `/askutd`) to invoke Lambda.
7. Enable CORS in API Gateway for frontend domain.

---

## Claude flow (independent setup)

Use file: `chat-handler/lambda_handler_claude.py`

1. In Bedrock console, request/access Claude model and create/select an inference profile.
2. Copy the inference profile ARN (or approved model ARN for your account/region).
3. In Lambda environment variables set:
   - `AWS_REGION` (example `us-east-1`)
   - `KNOWLEDGE_BASE_ID`
   - `MODEL_ARN` (Claude inference profile ARN)
4. Deploy code with `lambda_handler_claude.lambda_handler` as handler entry.
5. Test event:

```json
{
  "body": "{\"message\":\"What events are happening today?\"}"
}
```

---

## Gemma flow (independent setup)

Use file: `chat-handler/lambda_handler_gemma.py`

1. In Bedrock console, request/access Gemma model in your region.
2. In Lambda environment variables set:
   - `AWS_REGION` (example `us-east-1`)
   - `KNOWLEDGE_BASE_ID`
   - Optional `MODEL_ID` (default is `google.gemma-3-4b-it`)
3. Deploy code with `lambda_handler_gemma.lambda_handler` as handler entry.
4. Test event:

```json
{
  "body": "{\"message\":\"Where can I get lunch near ECSW?\"}"
}
```

---

## Common issues and fixes

1. `Missing KNOWLEDGE_BASE_ID`
   - Add `KNOWLEDGE_BASE_ID` in Lambda environment variables.
2. `Missing MODEL_ARN` (Claude)
   - Add valid Claude inference profile ARN to `MODEL_ARN`.
3. `AccessDeniedException`
   - Update Lambda IAM role with Bedrock permissions.
4. `ValidationException` for model ARN/region
   - Ensure model access is enabled in the same region as Lambda and KB.
5. Empty or irrelevant responses
   - Re-sync KB data source.
   - Verify JSON files are in the KB data source path.
6. Frontend gets CORS error
   - Enable CORS headers in API Gateway and keep `Access-Control-Allow-Origin` in Lambda response.

---

## Run and verify (end)

1. Deploy one handler (Claude or Gemma).
2. Confirm API Gateway integration points to that Lambda.
3. Open frontend and send:
   - `Where can I get vegetarian lunch near ECSS?`
   - `What events are happening today?`
   - `Where can I park near ECSW?`
4. Confirm HTTP 200 and useful response text in UI and CloudWatch logs.
