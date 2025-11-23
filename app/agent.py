from typing import Dict, List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

from .config_agent import agent_settings

# Histórico simples em memória: session_id -> lista de linhas de texto
_sessions_history: Dict[str, List[str]] = {}


def get_history(session_id: str) -> List[str]:
    """Devolve (ou cria) o histórico de conversa para uma sessão."""
    if session_id not in _sessions_history:
        _sessions_history[session_id] = []
    return _sessions_history[session_id]


def update_history(session_id: str, user_question: str, answer: str) -> None:
    """Atualiza o histórico de uma sessão com a nova pergunta e resposta."""
    history = get_history(session_id)
    history.append(f"Utilizador: {user_question}")
    history.append(f"Assistente: {answer}")


def get_retriever():
    """
    Carrega a base vetorial Chroma do disco e devolve um retriever.
    Usa o MESMO modelo de embeddings que foi usado na ingestão (Hugging Face).
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=agent_settings.CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name=agent_settings.COLLECTION_NAME,
    )

    return vectordb.as_retriever(search_kwargs={"k": 4})


def build_prompt(session_id: str, question: str, docs) -> str:
    """Constrói o prompt manual para o LLM (contexto + histórico + pergunta)."""
    history_lines = get_history(session_id)
    last_history = "\n".join(history_lines[-8:]) if history_lines else "Sem histórico prévio."

    context_parts = []
    for i, doc in enumerate(docs[:4]):
        text = doc.page_content
        if len(text) > 800:
            text = text[:800] + "..."
        context_parts.append(f"[Trecho {i+1}]\n{text}")
    context = "\n\n".join(context_parts) if context_parts else "Nenhum trecho encontrado."

    prompt = f"""
Tu és um assistente de auditoria especializado em normas ISSAI / auditoria de desempenho.

Contexto das normas:
{context}

Histórico:
{last_history}

Pergunta:
{question}

Instruções:
- Responde em português claro.
- Usa apenas os trechos recuperados como base factual.
- Refere a norma (ex.: ISSAI 300) quando fizer sentido.
"""
    return prompt


def ask_agent(session_id: str, question: str) -> str:
    """RAG + memória + chamada ao LLM."""
    if not agent_settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não definido. Verifica o .env.")

    # 1) Recuperar trechos relevantes
    retriever = get_retriever()
    docs = retriever.invoke(question)

    # 2) Construir prompt
    prompt = build_prompt(session_id, question, docs)

    # 3) Chamar LLM
    llm = ChatOpenAI(
        api_key=agent_settings.OPENAI_API_KEY,
        model=agent_settings.OPENAI_MODEL,
        temperature=0.2,
    )
    response = llm.invoke(prompt)
    answer = response.content

    # 4) Atualizar memória
    update_history(session_id, question, answer)

    return answer
