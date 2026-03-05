# UTD AI Campus Assistant — Setup & Replication Guide

This guide walks you through connecting your existing local frontend to a fully functional AWS backend, entirely configured via the AWS Management Console.

### Assumptions:
1. You already have the **GitHub repository** code downloaded locally on your computer. (https://github.com/Sinmisworld/utd-aws-cloud-club-ai-campus-assistant.git)
2. Make sure you have three json files in <utd-aws-cloud-club-ai-campus-assistant\data-storage\sample-data>
3. You have an active **AWS account** and are logged into the AWS Console.

---
## Step - 0
1. Create an IAM user

## Step 1 — Create the S3 Data Bucket

This bucket will store the data files that power the AI's knowledge base.

1. Go to **AWS Console → S3 → Create bucket**
2. Name it something unique, e.g. `utd-campus-assistant-data-<your-id>`.
3. Choose your preferred region (e.g., **us-east-2**) and click **Create bucket**.
4. **Upload your data files** (the ones containing campus info) directly into this new bucket.

---

## Step 3 — Create a Bedrock Knowledge Base

1. Go to **AWS Console → Amazon Bedrock → Knowledge bases** 
2. Click **Create knowledge base with type = KB with vector store**.
3. Configure: 
   - **Name**: `utd-campus-assistant-kb`
   - **IAM role**: Let AWS create a new service role
   - **Data source**: Select **Amazon S3**
   - **S3 URI**: Enter the bucket you created in Step 1 (e.g., `s3://utd-campus-assistant-data-<your-id>/`)
   - **Embedding model**: Pick a supported default model like **Titan Embeddings G1 — Text**
   - **Vector store**: Use the s3 vector store.
4. Click **Create knowledge base**.
5. Once created, click **Sync** on the data source to process your uploaded files. 
6. Go to data sources - click on kb and sync
7. **Save your Knowledge Base ID** (a ~10 character string at the top of the details page) 

---

## Step 4 — Create the Lambda Function

1. Go to **AWS Console → Lambda → Create function**.
2. Configure:
   - **Function name**: `askutd`
   - **Runtime**: **Python 3.11** 
   - **Execution role**: Create a new role with basic Lambda permissions
3. Click **Create function**.
4. After this go to bedrock -> Inference Profiles -> choose sonnet 4.6 -> copy inference profile arn 

### Configure Lambda Code & Environment
1. In the Lambda physical file editor, **paste the code** from your local [backend/chat-handler/app.py] file to replace the default code. (Change your kb key on line 13 followed by entereing model arn)
2. Click **Deploy**.
3. Go to **Configuration → Environment variables → Edit** and add:
5. Increase the **Timeout** to **1 minute** and **Memory** to **256 MB**. Click **Save**.
Increate the time-out to a min
   - `KNOWLEDGE_BASE_ID`: *<The ID from Step 3>*
   - `AWS_REGION`: *<Your region, e.g., us-east-2>*
4. Click **Save**.

### Configure Lambda Permissions & Settings
1. Go to **Configuration → Permissions**. Click the execution role link to open IAM.
2. Under **Permissions policies**, click **Add permissions → Attach Policy → 'BedRockFullAccess**.
3. 
```
TEST
{
  "body": {
    "message": "Tell me about yourself"    
  }
}
```

## Step 5 — Create API Gateway

1. Go to **AWS Console → API Gateway → Create API**.
2. Choose **REST API** and click **Build**.
3. Name it `utd-campus-assistant-api` (Endpoint type: Regional), then click **Create API**.

### Setup the Endpoint
1. Click **Create Resource**.
   - **Resource path**: `/askutd`
   - ✅ Check **Enable API Gateway CORS**
   - Click **Create Resource**
2. Select the `/askutd` resource, click **Create Method**.
   - **Method type**: `POST`
   - **Integration type**: Lambda Function
   - **Lambda function**: Type in `askutd`
   - Click **Create method**

### Enable CORS & Deploy
1. Select the `/askutd` resource, click **Enable CORS**. Select every single option
2. Make sure `POST` and `OPTIONS` are checked. Set **Access-Control-Allow-Origin** to `*`. Click **Save**.
3. Click **Deploy API**.
4. Under **Stage**, select *New stage*, name it `dev`, and click **Deploy**.
5. **Copy the Invoke URL** at the top of the screen (it looks like `https://<id>.execute-api.<region>.amazonaws.com/dev/askutd`). <FILL YOU HERE - >

---

## Step 6 — Connect & Run Your Frontend

1. Open your local file: [frontend/public/app.js]
2. Update the `API_URL` on **line 6** with the Invoke URL you just copied:
```javascript
const API_URL = "https://<YOUR-API-ID>.execute-api.<YOUR-REGION>.amazonaws.com/dev/askutd";
```
3. Save the file.
4. **Test it locally!** Open your terminal, navigate to the frontend folder, and start a local server:
```bash
cd frontend/public
python -m http.server 8080
```
5. Visit `http://localhost:8080` in your browser. Try asking a question (e.g., *"Where can I get vegetarian lunch?"*) to verify the connection.

*(Optional)*: To host this publicly, you can create a second S3 bucket, enable "Static website hosting", unblock public access, add a public read bucket policy, and upload your entire `frontend/public/` folder to it.
