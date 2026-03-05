# UTD AWS Cloud Club – AI Campus Assistant

This repo contains the code and infrastructure for the **AI-powered UTD Campus Assistant** we’re building for the AWS Cloud Club workshop.

The goal is a **working, teachable demo** that shows how to connect:

- **Frontend** → web chatbot UI (S3 static site)
- **Backend** → API Gateway + Lambda
- **AI** → Amazon Bedrock (Claude 3.5 Sonnet)
- **Data** → Mock dining, events, and parking data (S3 or DynamoDB)
- **Infra** → Terraform or CDK to deploy everything

We are targeting **three main intents**:

1. Dining options (with simple dietary filters)
2. Events today/tomorrow
3. Parking status (mocked data)

## Repo Structure

- `frontend/` – Web chat UI (Frontend/UI Team)
- `backend/` – Chat handler + Lambda tools for dining/events/parking (Backend/API Team)
- `data-storage/` – Sample datasets & DynamoDB design (Data/Storage Team)
- `infra-deploy/` – Terraform + scripts to deploy stack (Infra & Deployment Team)
- `docs/` – Architecture, task breakdown, and workshop notes

## Teams

### 1. Frontend/UI Team (2–3)

**Folder:** `frontend/`

- Build a **single-page chat interface** (input, send button, chat bubbles).
- Call the `/chat` API endpoint exposed by API Gateway.
- Host static site on **S3** (CloudFront optional).
- Keep styling simple and readable (UTD colors if possible).

### 2. Backend/API Team (2–3)

**Folder:** `backend/`

- Implement a `chat-handler` Lambda:
  - Input: `{ "message": "Where can I park near ECSW?" }`
  - Calls **Bedrock** (Claude 3.5) with system prompt + tool schemas.
  - Routes to one of three tool Lambdas:
    - `DiningTool` – reads dining data.
    - `EventsTool` – reads event data.
    - `ParkingTool` – reads parking data.
  - Returns a structured response for the frontend to render.
- Keep everything as simple Python functions.

### 3. Data/Storage Team (2–3)

**Folder:** `data-storage/`

- Create **sample data**:
  - `dining.json`
  - `events.json`
  - `parking.json`
- Decide whether we store them in **S3** only (simpler) or **DynamoDB**.
- Document any DynamoDB tables (key schema, example items).

### 4. Infra & Deployment Team (2–3)

**Folder:** `infra-deploy/`

- Use **Terraform** (or CDK) to define:
  - S3 bucket (static site + data)
  - API Gateway + Lambda functions
  - IAM roles/policies
- Provide **deploy** and **destroy** scripts.
- Make it easy to spin this up in a single account for demo day.

## Development Flow

All members develop in their **own AWS accounts**.  
Final integration and deployment for the workshop happens in **one shared AWS account**.

Basic flow:

1. Each team builds and tests in their own space.
2. All changes merged into `main` branch.
3. Infra team runs `deploy.sh` in the shared account to stand up the demo environment.

## Minimum Demo Requirements

For the workshop, we want to be able to:

1. Ask: “Where can I get vegetarian lunch near ECSS?”  
   → See dining results from our dataset.

2. Ask: “What events are happening today?”  
   → See events filtered by today’s date.

3. Ask: “Where can I park near ECSW?”  
   → See mock parking lot availability.

If those three flows work end-to-end, we’re successful ✅
