const API_URL = "https://v05eylc2w3.execute-api.us-east-2.amazonaws.com/dev/askutd";

const chatEl = document.getElementById("chat");
const messageInputEl = document.getElementById("messageInput");
const composerFormEl = document.getElementById("composerForm");
const statusEl = document.getElementById("statusText");
const clearBtnEl = document.getElementById("clearBtn");
const promptGroupEl = document.getElementById("promptGroup");
const sendBtnEl = document.getElementById("sendBtn");

function setStatus(text) {
  statusEl.textContent = text;
}

function autoGrowTextarea() {
  messageInputEl.style.height = "auto";
  messageInputEl.style.height = Math.min(messageInputEl.scrollHeight, 150) + "px";
}

function addMessage(role, text) {
  const row = document.createElement("div");
  row.className = "message-row " + role;

  const bubble = document.createElement("div");
  bubble.className = "message " + role;
  bubble.textContent = text;

  row.appendChild(bubble);
  chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;

  if (promptGroupEl) {
    promptGroupEl.style.display = "none";
  }
}

function parseAnswerFromPayload(payload) {
  if (payload == null) {
    return "No response body received.";
  }

  if (typeof payload === "string") {
    const trimmed = payload.trim();
    if (!trimmed) {
      return "No response body received.";
    }

    try {
      const parsed = JSON.parse(trimmed);
      return parseAnswerFromPayload(parsed);
    } catch {
      return trimmed;
    }
  }

  if (Array.isArray(payload)) {
    if (payload.length === 0) {
      return "No response body received.";
    }
    return parseAnswerFromPayload(payload[0]);
  }

  if (typeof payload !== "object") {
    return String(payload);
  }

  if (payload.body !== undefined) {
    return parseAnswerFromPayload(payload.body);
  }

  if (payload.parsed_response !== undefined) {
    return parseAnswerFromPayload(payload.parsed_response);
  }

  if (payload.raw_response !== undefined) {
    return parseAnswerFromPayload(payload.raw_response);
  }

  if (payload.text !== undefined) {
    return parseAnswerFromPayload(payload.text);
  }

  return (
    payload.answer ||
    payload.message ||
    payload.response ||
    payload.reply ||
    JSON.stringify(payload)
  );
}

async function postMessage(message) {
  const resp = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      body: {
        message
      }
    })
  });

  const rawText = await resp.text();

  if (!resp.ok) {
    let reason = rawText || ("HTTP " + resp.status);
    try {
      const parsedError = JSON.parse(rawText);
      reason = parseAnswerFromPayload(parsedError);
    } catch {
      // Keep raw body when response is not valid JSON.
    }
    throw new Error(reason);
  }

  return parseAnswerFromPayload(rawText);
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) {
    return;
  }

  addMessage("user", message);
  messageInputEl.value = "";
  autoGrowTextarea();

  setStatus("Thinking...");
  sendBtnEl.disabled = true;
  addMessage("assistant", "...");

  try {
    const answer = await postMessage(message);
    const bubbles = chatEl.querySelectorAll(".message.assistant");
    bubbles[bubbles.length - 1].textContent = answer;
    setStatus("Done");
  } catch (error) {
    const bubbles = chatEl.querySelectorAll(".message.assistant");
    bubbles[bubbles.length - 1].textContent = "Error: " + (error.message || String(error));
    setStatus("Request failed");
  } finally {
    sendBtnEl.disabled = false;
  }
}

composerFormEl.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInputEl.value);
});

messageInputEl.addEventListener("input", autoGrowTextarea);

messageInputEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage(messageInputEl.value);
  }
});

clearBtnEl.addEventListener("click", () => {
  chatEl.innerHTML = "";
  if (promptGroupEl) {
    promptGroupEl.style.display = "";
  }
  setStatus("Cleared");
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    sendMessage(button.dataset.prompt || "");
  });
});

addMessage("assistant", "Hi! Ask me anything about UTD dining, events, parking, and campus life.");
setStatus("Ready");
autoGrowTextarea();
