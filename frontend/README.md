# Frontend (Chat UI)

This folder contains the static chatbot UI for the UTD Campus Assistant.

## Files

- `public/index.html`: page structure.
- `public/styles.css`: styling.
- `public/app.js`: chat logic and API call.

## How it works

1. User enters a message in the chat box.
2. `app.js` sends a `POST` request to API Gateway (`/askutd`).
3. Backend Lambda returns answer text/JSON.
4. UI renders the assistant response in the chat area.

## Configure backend endpoint

In `public/app.js`, set:

```js
const API_URL = "https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/askutd";
```

## Request format expected by current frontend

The frontend currently sends:

```json
{
  "body": {
    "message": "Where can I park near ECSW?"
  }
}
```

Backend handlers in `backend/chat-handler` are written to parse string/dict body safely.

## Common issues and fixes

1. Browser CORS error
   - Enable CORS in API Gateway and return `Access-Control-Allow-Origin` from Lambda.
2. `403`/`500` from API
   - Check Lambda logs in CloudWatch and verify API integration route.
3. Response appears blank
   - Check API response shape and verify `raw_response` or `parsed_response` exists.
4. Wrong endpoint/stage
   - Confirm `API_URL` includes the correct stage and route (`/askutd`).

## Run (end)

Serve `frontend/public` using any static server, then open the page in browser.

Example:

```powershell
cd frontend/public
python -m http.server 5500
```

Then open `http://localhost:5500` and test chatbot prompts.
