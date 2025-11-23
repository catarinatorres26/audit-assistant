# 🧾 Assistente de Auditoria (RAG + LLM)

Este projeto é um **assistente de auditoria** que funciona como um “copiloto” para auditores, permitindo fazer perguntas sobre normas de auditoria (por exemplo, ISSAI 300, GUID 2900) e obter respostas fundamentadas nos documentos oficiais.

A solução usa:

- **RAG (Retrieval-Augmented Generation)** com base vetorial em Chroma
- **Embeddings HuggingFace**
- **LLM da OpenAI** (ex.: `gpt-4o-mini`)
- **FastAPI** para expor uma API REST
- **Interface web de chat** (`/playground`)
- **Docker** para empacotamento e deploy em PaaS (ex.: Render)

---

## 🧱 Arquitetura (visão geral)

```mermaid
flowchart LR
    U[Utilizador\n(browser ou cliente HTTP)] -->|HTTP (GET/POST)| API[FastAPI\n(app.api)]

    subgraph Container["Container Docker\n(audit-assistant)"]
      API --> AGENT[Agente RAG\n(app.agent)]
      AGENT --> RETRIEVER[ChromaDB\n(vectordb)]
      AGENT --> LLM[OpenAI LLM\n(gpt-4o-mini)]
      RETRIEVER --> DOCS[(Normas de Auditoria\nPDFs -> chunks)]
    end

    U <-->|/playground\nUI de chat| API
