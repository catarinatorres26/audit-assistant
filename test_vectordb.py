from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import settings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=settings.CHROMA_DB_DIR,
    embedding_function=embeddings,
    collection_name=settings.COLLECTION_NAME,
)

print("Número de documentos na coleção:", db._collection.count())
