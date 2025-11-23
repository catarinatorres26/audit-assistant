import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import settings

DATA_DIR = "data/normas"


def load_documents():
    """Carrega todos os PDFs da pasta data/normas como Document objects do LangChain."""
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.lower().endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            print(f"Carregando PDF: {path}")
            loader = PyPDFLoader(path)
            pdf_docs = loader.load()
            docs.extend(pdf_docs)
    return docs


def split_documents(docs):
    """
    Divide os documentos em chunks menores.
    chunk_size: tamanho do pedaço em caracteres
    chunk_overlap: sobreposição entre chunks para não perder contexto.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Total de chunks gerados: {len(chunks)}")
    return chunks


def build_vector_store(chunks):
    """
    Cria embeddings locais (HuggingFace) e persiste tudo num ChromaDB local.
    NÃO usa OpenAI, logo não consome quota de API.
    """
    print("A inicializar modelo de embeddings (Hugging Face)...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name=settings.COLLECTION_NAME,
    )

    vectordb.persist()
    print(f"Base vetorial criada em {settings.CHROMA_DB_DIR}")
    return vectordb


if __name__ == "__main__":
    print("=== Início da ingestão de normas de auditoria (Hugging Face) ===")
    docs = load_documents()
    print(f"{len(docs)} documentos (páginas) carregados dos PDFs.")

    chunks = split_documents(docs)
    vectordb = build_vector_store(chunks)

    print("=== Ingestão concluída com sucesso. ===")
