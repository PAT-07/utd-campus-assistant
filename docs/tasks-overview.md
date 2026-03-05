# Tasks Overview

This document defines who does what for the UTD chatbot project and the order to deliver an end-to-end demo.

## Project goal

Ship a working UT Dallas chatbot that answers questions about:

1. Dining
2. Events
3. Parking

Using:

1. S3 for data
2. Bedrock Knowledge Base for retrieval
3. Lambda + API Gateway for backend API
4. Static web frontend for chat interface

## Workstreams

## 1) Data and Knowledge Base

Owner: Data/Storage team

Tasks:

1. Validate and maintain:
   - `data-storage/sample-data/dining.json`
   - `data-storage/sample-data/events.json`
   - `data-storage/sample-data/parking.json`
2. Upload files to S3 bucket/prefix.
3. Create Bedrock Knowledge Base and connect S3 data source.
4. Run KB sync and verify successful ingestion.
5. Share `KNOWLEDGE_BASE_ID` with backend team.

Definition of done:

1. KB status is active.
2. Sync succeeds with no ingestion errors.
3. Sample query in Bedrock KB returns relevant chunks.

## 2) Backend API

Owner: Backend team

Tasks:

1. Deploy Lambda chat handler:
   - Claude path: `backend/chat-handler/lambda_handler_claude.py`
   - Gemma path: `backend/chat-handler/lambda_handler_gemma.py`
2. Set Lambda environment variables:
   - `AWS_REGION`
   - `KNOWLEDGE_BASE_ID`
   - `ALLOW_ORIGIN`
   - `MODEL_ARN` (Claude) or `MODEL_ID` (Gemma)
3. Configure API Gateway route:
   - `POST /askutd`
4. Enable CORS and verify headers.
5. Confirm CloudWatch logs capture request/response and errors.

Definition of done:

1. API returns HTTP 200 for valid message payload.
2. API returns readable error for invalid payload.
3. Dining/events/parking prompts return model answers from KB context.

## 3) Frontend chat UI

Owner: Frontend team

Tasks:

1. Keep UI in:
   - `frontend/public/index.html`
   - `frontend/public/styles.css`
   - `frontend/public/app.js`
2. Set `API_URL` in `app.js` to deployed API Gateway endpoint.
3. Validate request and response parsing in browser.
4. Ensure mobile and desktop usability.

Definition of done:

1. User can send prompt and receive response in chat log.
2. Error states are visible (failed request, empty response).
3. Example prompts work end to end.

## 4) Integration and demo readiness

Owner: All teams

Tasks:

1. Confirm same AWS region across Lambda, KB, and model access.
2. Run final smoke tests:
   - `Where can I get vegetarian lunch near ECSS?`
   - `What events are happening today?`
   - `Where can I park near ECSW?`
3. Capture screenshots or short recording for demo backup.
4. Freeze config values before presentation.

Definition of done:

1. All three prompts return useful answers in frontend.
2. No blocking errors in CloudWatch during smoke tests.
3. Teams can explain architecture and fallback troubleshooting steps.

## Suggested implementation sequence

1. Prepare and upload data to S3.
2. Create and sync Bedrock Knowledge Base.
3. Deploy backend Lambda and API Gateway.
4. Point frontend `API_URL` to deployed API.
5. Execute smoke tests and fix issues.
6. Demo rehearsal.

## Common blockers checklist

1. `KNOWLEDGE_BASE_ID` missing or wrong.
2. Bedrock model access not enabled in selected region.
3. Wrong `MODEL_ARN` for Claude or unsupported `MODEL_ID` for Gemma.
4. API Gateway CORS misconfiguration.
5. Lambda role missing `bedrock:RetrieveAndGenerate`.
6. KB not re-synced after S3 data update.
