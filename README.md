# UTD AI Campus Assistant 🚀

An AI-powered campus assistant that helps students find information about dining, events, parking, and campus services at the University of Texas at Dallas.

This project demonstrates how to build a **serverless AI application on AWS** using Amazon Bedrock, Lambda, and API Gateway.

---

## 🧠 Architecture Overview

The application follows a simple **AI + Serverless architecture**:

User → Web Chat UI → API Gateway → Lambda → Amazon Bedrock → Knowledge Base → Response

### AWS Services Used

* Amazon Bedrock – AI model inference
* AWS Lambda – Serverless backend logic
* Amazon API Gateway – REST API for the chatbot
* Amazon S3 – Static frontend hosting and datasets
* Amazon CloudWatch – Logging and monitoring

---

## 💬 Features

The assistant can answer questions related to campus life such as:

* Dining options and dietary preferences
* Events happening today or tomorrow
* Parking availability near campus buildings

Example queries:

* "Where can I get vegetarian lunch near ECSS?"
* "What events are happening today?"
* "Where can I park near ECSW?"

---

## 🏗 Project Structure

```
utd-campus-assistant/
│
├── frontend/          # Chatbot UI (HTML, CSS, JavaScript)
├── backend/           # Lambda functions and API logic
├── data-storage/      # Sample campus datasets
├── docs/              # Architecture and project documentation
└── infra-deploy/      # Infrastructure scripts (Terraform/CDK)
```

---

## ⚙️ How It Works

1. The user sends a message from the **web chatbot interface**.
2. The request is sent to **Amazon API Gateway**.
3. API Gateway triggers a **Lambda function**.
4. The Lambda function calls **Amazon Bedrock** to process the query.
5. Bedrock retrieves relevant campus information from the dataset.
6. A response is returned to the chatbot UI.

---

## 🚀 Running the Project Locally

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/utd-campus-assistant.git
cd utd-campus-assistant/frontend/public
```

Start a local server:

```
python -m http.server 8080
```

Open in browser:

```
http://localhost:8080
```

---

## 📊 Example Architecture

Frontend (Static Website)
↓
Amazon API Gateway
↓
AWS Lambda (Chat Handler)
↓
Amazon Bedrock Model
↓
Campus Knowledge Base

---

## 📚 Learning Goals

This project demonstrates:

* Building **AI applications with Amazon Bedrock**
* Implementing **serverless backend architectures**
* Integrating **frontend applications with cloud APIs**
* Designing a simple **retrieval-based AI assistant**

---

## 👨‍💻 Author

Pratyaksh Singh
MS Information Technology Management – UT Dallas

GitHub: https://github.com/PAT-07
