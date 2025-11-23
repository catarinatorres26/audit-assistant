from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .schemas import ChatRequest, ChatResponse
from .agent import ask_agent
from .config_agent import agent_settings

app = FastAPI(
    title="Assistente de Auditoria",
    description=(
        "API do assistente de auditoria com RAG (Chroma + HuggingFace) e memória de conversação.\n\n"
        "Use o endpoint /chat para colocar perguntas sobre normas de auditoria "
        "(por exemplo, ISSAI 300, GUID 2900, etc.)."
    ),
    version="0.1.0",
    contact={
        "name": "Audit Assistant",
        "email": "example@example.com",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", response_class=HTMLResponse, tags=["UI"])
def landing_page():
    """Página simples de boas-vindas, com layout melhorado (sem .format, sem f-strings)."""
    model = agent_settings.OPENAI_MODEL
    vectordb = agent_settings.CHROMA_DB_DIR
    collection = agent_settings.COLLECTION_NAME

    html = """
    <!DOCTYPE html>
    <html lang="pt">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Assistente de Auditoria</title>
        <style>
          :root {
            color-scheme: light dark;
          }
          * {
            box-sizing: border-box;
          }
          body {
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, #eef3ff 0, #dde4ff 22%, #f5f7fb 60%, #ffffff 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .page {
            max-width: 900px;
            width: 100%;
            padding: 2rem;
          }
          .card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 18px;
            padding: 2rem 2.4rem;
            box-shadow: 0 14px 45px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.25);
          }
          h1 {
            margin-top: 0;
            margin-bottom: 0.5rem;
            font-size: 2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #0f172a;
          }
          h1 span.emoji {
            font-size: 1.8rem;
          }
          p.subtitle {
            margin-top: 0;
            margin-bottom: 1.5rem;
            color: #475569;
          }
          .section-title {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.4rem;
          }
          ul.links {
            list-style: none;
            padding-left: 0;
            margin-top: 0.4rem;
            margin-bottom: 1.4rem;
          }
          ul.links li {
            margin-bottom: 0.25rem;
          }
          ul.links a {
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
          }
          ul.links a:hover {
            text-decoration: underline;
          }
          .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1.2rem;
          }
          .badge {
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.7);
            color: #475569;
            background: rgba(248, 250, 252, 0.9);
          }
          .code-box {
            background: #0f172a;
            color: #e5e7eb;
            border-radius: 12px;
            padding: 0.9rem 1.1rem;
            font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.8rem;
            overflow-x: auto;
            margin-top: 0.4rem;
          }
          .code-box code {
            white-space: pre;
          }
          .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.06);
            color: #1d4ed8;
            font-size: 0.78rem;
            font-weight: 500;
            margin-bottom: 0.8rem;
          }
          .pill span {
            font-size: 0.95rem;
          }
          .footer {
            margin-top: 1.6rem;
            font-size: 0.78rem;
            color: #94a3b8;
          }
          @media (max-width: 640px) {
            .card {
              padding: 1.5rem 1.4rem;
            }
          }
        </style>
      </head>
      <body>
        <div class="page">
          <div class="card">
            <h1>
              <span class="emoji">🧾</span>
              Assistente de Auditoria
            </h1>
            <p class="subtitle">
              Copiloto de auditoria com RAG (Chroma + HuggingFace) e memória de conversação,
              focado em normas de auditoria (por exemplo, ISSAI 300, GUID 2900).
            </p>

            <div class="pill">
              <span>⚙️</span> API pronta para integração (FastAPI + AWS Lambda friendly)
            </div>

            <div class="badge-row">
    """

    html += (
        f'              <div class="badge">LLM: {model}</div>\n'
        f'              <div class="badge">Vector Store: {vectordb}</div>\n'
        f'              <div class="badge">Coleção: {collection}</div>\n'
    )

    html += """
            </div>

            <div>
              <div class="section-title">Navegação rápida</div>
              <ul class="links">
                <li><b>Estado da API:</b> <a href="/health">/health</a></li>
                <li><b>Documentação interativa (Swagger):</b> <a href="/docs">/docs</a></li>
                <li><b>Documentação alternativa (ReDoc):</b> <a href="/redoc">/redoc</a></li>
              </ul>
            </div>

            <div>
              <div class="section-title">Exemplo de chamada ao endpoint /chat</div>
              <div class="code-box">
                <code>
curl -X POST "http://localhost:8000/chat" \\
  -H "Content-Type: application/json" \\
  -d '{
    "session_id": "sessao-auditor-123",
    "question": "Quais são os princípios da auditoria de desempenho na ISSAI 300?"
  }'
                </code>
              </div>
            </div>

            <div class="footer">
              Desenvolvido para demonstração de um agente de IA aplicado à auditoria, com foco em
              raciocínio apoiado em normas e transparência na fonte da informação.
            </div>
          </div>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/health", tags=["Sistema"])
def health_check():
    """Verifica se a API está operacional e devolve algumas informações básicas."""
    return {
        "status": "ok",
        "model": agent_settings.OPENAI_MODEL,
        "chromadb_dir": agent_settings.CHROMA_DB_DIR,
        "collection": agent_settings.COLLECTION_NAME,
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat_endpoint(payload: ChatRequest):
    """
    Endpoint principal de chat com o assistente de auditoria.

    - Usa RAG (Chroma + embeddings Hugging Face)
    - Mantém memória por `session_id`
    - Responde em português com base nas normas carregadas
    """
    answer = ask_agent(session_id=payload.session_id, question=payload.question)
    return ChatResponse(
        session_id=payload.session_id,
        question=payload.question,
        answer=answer,
        model=agent_settings.OPENAI_MODEL,
    )

@app.get("/playground", response_class=HTMLResponse, tags=["UI"])
def chat_playground():
    """Interface simples de chat no browser que consome o endpoint /chat."""
    html = """
    <!DOCTYPE html>
    <html lang="pt">
      <head>
        <meta charset="UTF-8" />
        <title>Assistente de Auditoria - Playground</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
          * {
            box-sizing: border-box;
          }
          body {
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, #eef3ff 0, #dde4ff 22%, #f5f7fb 60%, #ffffff 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .shell {
            max-width: 960px;
            width: 100%;
            padding: 2rem 1.5rem;
          }
          .card {
            background: rgba(255,255,255,0.96);
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12);
            border: 1px solid rgba(148, 163, 184, 0.35);
            padding: 1.75rem 1.75rem 1.5rem;
            display: grid;
            grid-template-rows: auto 1fr auto;
            gap: 1rem;
            height: 80vh;
          }
          .header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 0.75rem;
          }
          .title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
          }
          .title span.emoji {
            font-size: 1.6rem;
          }
          .title h1 {
            font-size: 1.3rem;
            margin: 0;
            color: #0f172a;
          }
          .subtitle {
            margin: 0;
            color: #64748b;
            font-size: 0.85rem;
          }
          .link-docs {
            font-size: 0.8rem;
          }
          .link-docs a {
            color: #2563eb;
            text-decoration: none;
          }
          .link-docs a:hover {
            text-decoration: underline;
          }
          .chat-window {
            background: #f8fafc;
            border-radius: 12px;
            padding: 0.75rem;
            overflow-y: auto;
            border: 1px solid rgba(148, 163, 184, 0.35);
          }
          .msg {
            margin-bottom: 0.75rem;
            max-width: 80%;
            padding: 0.6rem 0.8rem;
            border-radius: 12px;
            font-size: 0.9rem;
            line-height: 1.35;
          }
          .msg.user {
            margin-left: auto;
            background: #2563eb;
            color: white;
            border-bottom-right-radius: 4px;
          }
          .msg.bot {
            margin-right: auto;
            background: white;
            border-bottom-left-radius: 4px;
            border: 1px solid rgba(148, 163, 184, 0.4);
          }
          .msg small {
            display: block;
            opacity: 0.7;
            font-size: 0.7rem;
            margin-top: 0.25rem;
          }
          .input-area {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 0.5rem;
            align-items: flex-end;
          }
          textarea {
            width: 100%;
            min-height: 3rem;
            max-height: 7rem;
            resize: vertical;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.7);
            padding: 0.6rem 0.75rem;
            font-family: inherit;
            font-size: 0.9rem;
          }
          button {
            border-radius: 999px;
            border: none;
            padding: 0.65rem 1.2rem;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            background: #2563eb;
            color: white;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
          }
          button:disabled {
            opacity: 0.6;
            cursor: default;
          }
          .small-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #94a3b8;
          }
          .session-id {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
          }
          @media (max-width: 640px) {
            .card {
              height: 90vh;
              padding: 1.25rem 1.25rem 1rem;
            }
            .title h1 {
              font-size: 1.1rem;
            }
          }
        </style>
      </head>
      <body>
        <div class="shell">
          <div class="card">
            <div class="header">
              <div>
                <div class="title">
                  <span class="emoji">🧾</span>
                  <h1>Assistente de Auditoria</h1>
                </div>
                <p class="subtitle">
                  Faz perguntas sobre normas de auditoria (ISSAI 300, GUID 2900, etc.) e vê as respostas aqui.
                </p>
              </div>
              <div class="link-docs">
                <a href="/docs" target="_blank">Ver documentação da API →</a>
              </div>
            </div>

            <div id="chat" class="chat-window">
              <div class="msg bot">
                Bem-vindo/a! 👋<br/>
                Coloca uma pergunta sobre normas de auditoria e eu respondo com base na base de conhecimento carregada.
                <small>Assistente</small>
              </div>
            </div>

            <div>
              <div class="input-area">
                <textarea id="question" placeholder="Escreve aqui a tua pergunta..."></textarea>
                <button id="sendBtn">
                  <span>Enviar</span> <span>➤</span>
                </button>
              </div>
              <div class="small-row">
                <span>As respostas são geradas com um modelo LLM e documentos de normas.</span>
                <span class="session-id" id="sessionLabel"></span>
              </div>
            </div>
          </div>
        </div>

        <script>
          const chatEl = document.getElementById("chat");
          const questionEl = document.getElementById("question");
          const sendBtn = document.getElementById("sendBtn");
          const sessionId = "web-" + Math.random().toString(36).slice(2, 10);
          document.getElementById("sessionLabel").textContent = "Sessão: " + sessionId;

          function addMessage(text, sender) {
            const div = document.createElement("div");
            div.classList.add("msg");
            div.classList.add(sender === "user" ? "user" : "bot");
            div.innerHTML = text + '<small>' + (sender === "user" ? "Tu" : "Assistente") + "</small>";
            chatEl.appendChild(div);
            chatEl.scrollTop = chatEl.scrollHeight;
          }

          async function sendQuestion() {
            const q = questionEl.value.trim();
            if (!q) return;
            addMessage(q, "user");
            questionEl.value = "";
            questionEl.focus();
            sendBtn.disabled = true;

            try {
              const resp = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  session_id: sessionId,
                  question: q
                })
              });

              if (!resp.ok) {
                const errText = await resp.text();
                addMessage("Ocorreu um erro na API: " + errText, "bot");
              } else {
                const data = await resp.json();
                addMessage(data.answer, "bot");
              }
            } catch (e) {
              addMessage("Erro de rede ao contactar o servidor.", "bot");
            } finally {
              sendBtn.disabled = false;
            }
          }

          sendBtn.addEventListener("click", sendQuestion);
          questionEl.addEventListener("keydown", function(ev) {
            if (ev.key === "Enter" && !ev.shiftKey) {
              ev.preventDefault();
              sendQuestion();
            }
          });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
