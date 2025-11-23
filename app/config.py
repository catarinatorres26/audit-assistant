class Settings:
    # Diretório onde o Chroma vai guardar a base vetorial
    CHROMA_DB_DIR: str = "vectordb"
    # Nome da coleção (podes mudar se quiseres separar projetos)
    COLLECTION_NAME: str = "normas_auditoria"

settings = Settings()
