import os

DATA_PATH = "input"
DB_PATH = "vector_db"
# MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
EMBEDDING_MODELS=["llama3.2:3b","nomic-embed-text"]
MODEL_COLLECTIONS=["gemma3:1b","gemma3:4b","llama3.2:3b"]
collections=["resume_collection","langchain"]

# Check if fine-tuned model exists, otherwise use base model
FINE_TUNED_MODEL_PATH = "fine_tuned_model"

EMBEDDING_MODEL_NAME = "nomic-embed-text"

# MODEL_NAME = "llama3.2:3b"
# MODEL_NAME = "gemma3:4b"
# MODEL_NAME = "qwen2.5:7b"
MODEL_NAME = "gemini"
# MODEL_NAME = "gemma3:1b"
# gemma3:1b use it
# MODEL_NAME = "llama3:8b"
PARSER_LIST=["marker","docling"]
PARSER=PARSER_LIST[0]
DB_NAME="db.db"

SQL_MODEL="qwen2.5-coder:3b"

COLLECTION_NAME="resume_collection"