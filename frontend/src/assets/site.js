const apiBaseUrl =
  typeof window !== "undefined" && window.__INTERACTIVE_RESUME_API__
    ? window.__INTERACTIVE_RESUME_API__
    : "http://127.0.0.1:8788";
const sessionId =
  typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
let latestSources = [];

export function citationParts(text) {
  const parts = [];
  const pattern = /\[(S[0-9]+)\]/g;
  let lastIndex = 0;
  for (const match of text.matchAll(pattern)) {
    if (match.index > lastIndex) {
      parts.push({ type: "text", value: text.slice(lastIndex, match.index) });
    }
    parts.push({ type: "citation", id: match[1] });
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    parts.push({ type: "text", value: text.slice(lastIndex) });
  }
  return parts;
}

function byId(id) {
  return document.getElementById(id);
}

function renderAnswer(answer, sources) {
  const panel = byId("answerPanel");
  panel.replaceChildren();
  for (const part of citationParts(answer)) {
    if (part.type === "text") {
      panel.append(document.createTextNode(part.value));
    } else {
      const button = document.createElement("button");
      button.className = "citation";
      button.type = "button";
      button.textContent = part.id;
      button.addEventListener("click", () => openSource(part.id));
      panel.append(button);
    }
  }
  if (!sources.length) {
    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = "No sources were returned for this answer.";
    panel.append(note);
  }
}

function openSource(id) {
  const source = latestSources.find((item) => item.id === id);
  if (!source) return;
  byId("drawerTitle").textContent = `${source.id}: ${source.title}`;
  byId("drawerUrl").textContent = source.url || "No public URL supplied.";
  byId("drawerBody").textContent = source.body_text || source.excerpt || "No source text available.";
  byId("sourceDrawer").showModal();
}

async function checkHealth() {
  const badge = byId("healthBadge");
  try {
    const response = await fetch(`${apiBaseUrl}/health`);
    if (!response.ok) throw new Error("Health check failed");
    const data = await response.json();
    badge.textContent = data.generation_provider === "placeholder" ? "API: placeholder" : "API: online";
    badge.className = "health online";
  } catch {
    badge.textContent = "API: offline";
    badge.className = "health offline";
  }
}

async function askQuestion(event) {
  event.preventDefault();
  const panel = byId("answerPanel");
  const message = byId("questionInput").value.trim();
  if (!message) return;
  panel.textContent = "Thinking...";
  try {
    const response = await fetch(`${apiBaseUrl}/chat`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        message,
        role: byId("roleSelect").value,
        model_profile: byId("profileSelect").value,
        session_id: sessionId
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error?.message || "Request failed");
    latestSources = data.sources || [];
    renderAnswer(data.answer, latestSources);
  } catch (error) {
    panel.innerHTML = "";
    const messageNode = document.createElement("p");
    messageNode.className = "muted";
    messageNode.textContent = `The live API is unavailable or returned an error: ${error.message}`;
    panel.append(messageNode);
  }
}

if (typeof document !== "undefined") {
  byId("questionForm").addEventListener("submit", askQuestion);
  byId("closeDrawer").addEventListener("click", () => byId("sourceDrawer").close());
  checkHealth();
}
