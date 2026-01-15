import os
from config import DATA_PATH, DB_PATH, EMBEDDING_MODEL_NAME, COLLECTION_NAME
from functions.ingestion_utils import (
    load_documents,
    load_documents_with_docling,
    split_by_headers,
    generate_chunk_ids,
    reset_vector_db,
    save_chunks_for_bm25,
    create_and_persist_db
)

def create_vector_db():
    # 1. Validation
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Directory '{DATA_PATH}' created. Please add PDF resumes there.")
        return

    print("Starting fresh ingestion with Semantic Sectioning...")

    # 2. Loading & Preprocessing
    # documents = load_documents(DATA_PATH)
    documents = load_documents_with_docling(DATA_PATH)
    if not documents:
        return


    # 3. Splitting
    print("Splitting text by Resume Sections...")
    chunks = split_by_headers(documents)
    chunks = generate_chunk_ids(chunks)
    print(f"Created {len(chunks)} semantic chunks.")

    # 4. Database Prep
    reset_vector_db(DB_PATH)
    save_chunks_for_bm25(chunks, DB_PATH)

    # 5. Vector Store Creation
    create_and_persist_db(
        chunks=chunks,
        db_path=DB_PATH,
        collection_name=COLLECTION_NAME,
        model_name=EMBEDDING_MODEL_NAME
    )

print()
if __name__ == "__main__":
    print("Starting ingestion process...")
    create_vector_db()