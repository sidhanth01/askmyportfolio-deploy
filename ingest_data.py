import os
import traceback
from dotenv import load_dotenv
from glob import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Updated import for latest embedding support
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

try:
    from langchain.document_loaders import UnstructuredMarkdownLoader
except ImportError:
    raise ImportError(
        "UnstructuredMarkdownLoader is missing. Please run: pip install unstructured"
    )

DATA_PATH = "data/"
CHROMA_DB_PATH = "chroma_db/"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Loader definitions: file pattern, loader class
SUPPORTED_TYPES = [
    ("**/*.pdf", PyPDFLoader),
    ("**/*.md", UnstructuredMarkdownLoader),
    ("**/*.txt", TextLoader),
]

def log(msg, level="info"):
    """Color-coded logging for terminal output."""
    color = {"info":"\033[96m", "warn":"\033[93m", "error":"\033[91m", "ok":"\033[92m"}
    print(f"{color.get(level, '')}{msg}\033[0m")

def find_files(root_dir, pattern):
    return glob(os.path.join(root_dir, pattern), recursive=True)

def load_documents():
    log("\n--- Starting Document Loading ---")
    all_docs, error_files = [], []
    for pattern, loader_cls in SUPPORTED_TYPES:
        files = find_files(DATA_PATH, pattern)
        if not files:
            log(f"  - No files found for {pattern}", "warn")
        for path in files:
            try:
                loader = loader_cls(path)
                loaded = loader.load()
                for doc in loaded if isinstance(loaded, list) else [loaded]:
                    doc.metadata.update({
                        "source_file": os.path.relpath(path, DATA_PATH),
                        "file_type": os.path.splitext(path)[1][1:]
                    })
                    all_docs.append(doc)
            except Exception as e:
                error_files.append((path, str(e)))
                log(f"  - Error loading {path}:", "error")
                traceback.print_exc()
    if not all_docs:
        log(f"No documents found in '{DATA_PATH}'. Place your files there.", "error")
    else:
        log(f"{len(all_docs)} files loaded from '{DATA_PATH}'.", "ok")
    if error_files:
        log(f"\nFiles failed to load ({len(error_files)}):", "warn")
        for file, err in error_files:
            log(f"  - {file}: {err}", "warn")
    return all_docs

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    log("\n--- Starting Document Splitting ---")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap,
        length_function=len, add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    # Deduplicate by stripped chunk text hash
    unique_chunks = {hash(d.page_content.strip()): d for d in chunks}
    log(f"Documents split into {len(unique_chunks)} unique chunks.", "ok")
    return list(unique_chunks.values())

def create_embeddings_and_store(chunks):
    log(f"\n--- Embedding and Persisting in ChromaDB ---", "info")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=CHROMA_DB_PATH
    )
    log(f"ChromaDB updated at '{CHROMA_DB_PATH}' with {len(chunks)} chunks.", "ok")
    return db

if __name__ == "__main__":
    load_dotenv()  # Ensure env is loaded if run standalone
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    log("Starting the data ingestion process...", "info")
    documents = load_documents()
    if documents:
        chunks = split_documents(documents)
        db = create_embeddings_and_store(chunks)
        log("\n--- Data Ingestion Complete! ---", "ok")
        log(f"Your vector DB is ready at '{CHROMA_DB_PATH}'. Start your Streamlit app.", "ok")
    else:
        log("\n--- Data Ingestion Skipped ---", "warn")
        log(f"No documents found to process. Place files in '{DATA_PATH}'.", "warn")
