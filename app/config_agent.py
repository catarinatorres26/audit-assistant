import os
from dotenv import load_dotenv

# Caminho absoluto para a raiz do projeto (onde está o .env)
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Carregar o .env explicitamente
load_dotenv(dotenv_path=ENV_PATH)


class AgentSettings:
    # OpenAI (LLM)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Chroma (base vetorial já criada na Fase 1)
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "vectordb")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "normas_auditoria")


agent_settings = AgentSettings()

# Debug opcional (não mostra a chave)
if not agent_settings.OPENAI_API_KEY:
    print("⚠️ [config_agent] OPENAI_API_KEY não foi carregada. Verifica o .env.")
else:
    print("✅ [config_agent] OPENAI_API_KEY carregada (valor escondido).")
