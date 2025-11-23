from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Identificador da sessão de conversa (pode ser um ID de utilizador ou um UUID).",
        example="sessao-auditor-123",
    )
    question: str = Field(
        ...,
        description="Pergunta do auditor sobre normas / auditoria de desempenho.",
        example="Quais são os princípios da auditoria de desempenho na ISSAI 300?",
    )


class ChatResponse(BaseModel):
    session_id: str = Field(
        ...,
        description="ID da sessão usada na pergunta.",
        example="sessao-auditor-123",
    )
    question: str = Field(
        ...,
        description="Pergunta original enviada pelo utilizador.",
        example="Quais são os princípios da auditoria de desempenho na ISSAI 300?",
    )
    answer: str = Field(
        ...,
        description="Resposta do assistente de auditoria, em português.",
        example="A ISSAI 300 estabelece três princípios base para a auditoria de desempenho: economicidade, eficiência e eficácia...",
    )
    model: str = Field(
        ...,
        description="Modelo LLM utilizado para gerar a resposta.",
        example="gpt-4o-mini",
    )
