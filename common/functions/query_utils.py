import pickle
import os
import sys
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder
# Ensure 'common' directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PATH, DB_PATH, EMBEDDING_MODEL_NAME, MODEL_NAME,COLLECTION_NAME,DB_NAME
import functions.database_utils as db_utils


CHUNKS_FILE = os.path.join(DB_PATH, "chunks.pkl")

PROMPT_TEMPLATE = """
Answer the question based only on the following context.
If the answer cannot be found, say "I cannot find this information in the provided resumes."

Context:
{context}

Question: {question}

Answer (include source filenames as evidence):
"""

def load_bm25_chunks():
    """Lengths and loads chunks for BM25 retrieval."""
    if not os.path.exists(CHUNKS_FILE):
        print(f"Chunks file not found at {CHUNKS_FILE}. Run ingest.py first.")
        return None
    
    with open(CHUNKS_FILE, "rb") as f:
        return pickle.load(f)

def get_bm25_results(chunks, query_text):
    """Retrieves documents using BM25."""
    if not chunks: 
        return []
    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = 10
    return retriever.invoke(query_text)

def get_vector_results(query_text,section_list=[]):
    """Retrieves documents using vector similarity."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
    # use NER to get the section
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings, collection_name=COLLECTION_NAME)
    lst=[{"section": x} for x in section_list]
    filter=None
    if len(section_list)==1:
        filter=lst[0]
    elif len(section_list)>1:
        filter={
            "$or": lst
        }
    results = db.similarity_search_with_score(
        query_text,
        k=10,
        filter=filter
    )  
    return [doc for doc, score in results if score > 0.75]

def merge_and_deduplicate(bm25_docs, vector_docs):
    """Merges and deduplicates documents by content."""
    seen = set()
    merged = []
    for doc in bm25_docs + vector_docs:
        h = hash(doc.page_content)
        if h not in seen:
            seen.add(h)
            merged.append(doc)
    return merged

def rerank_documents(query_text, docs):
    """Reranks documents using CrossEncoder."""
    if not docs:
        return []
        
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
    pairs = [[query_text, doc.page_content] for doc in docs]
    scores = reranker.predict(pairs)
    
    # Sort and take top 5
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:5]]

def merge_same_source(docs):
    """Merges documents with the same source."""
    merge_dict={}
    for doc in docs:
        source = doc.metadata.get('source', 'Unknown')
        if(merge_dict[source]):
            merge_dict[source].page_content += "\n\n" + doc.page_content
        else:
            merge_dict[source] = doc
    return list(merge_dict.values())



def get_connection():
    return db_utils.get_db_connection(DB_NAME)


def generate_answer(query_text, context_docs):
    """Generates answer using LLM."""
    context_list = []
    email_group_content_dict={}
    for doc in context_docs:
        # check if email is already in the dictionary
        if doc.metadata.get("email", "Unknown") in email_group_content_dict:
            email_group_content_dict[doc.metadata.get("email", "Unknown")].append(doc)
        else:
            email_group_content_dict[doc.metadata.get("email", "Unknown")]=[doc]

    with get_connection() as conn:
        for email in email_group_content_dict:
            sql_data=db_utils.get_data_by_email(conn,email)
            result=f"""
            This is the cv of {sql_data[0]["general"]["name"]}
            # Personal information
             Name: {sql_data[0]["general"]["name"]}
             Email: {sql_data[0]["general"]["email"]}
            """
            for doc in email_group_content_dict[email]:
                result+=f"\n\n# {doc.metadata.get("section", "contents")}\n\n{doc.page_content}"
            context_list.append(result)
           

    context_text = "\n\n---\n\n".join(context_list)

   
    
    template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = template.format(context=context_text, question=query_text)
    
    print(f"\nGenerating answer using {MODEL_NAME}...\n")
    model = ChatOllama(model=MODEL_NAME)
    response = model.invoke(prompt)
    content=response.content
     #  write to a log file
    with open("log.txt", "a") as f:
        f.write(f"Query: {query_text}\n")
        f.write(f"Context: {context_text}\n")
        f.write(f"Answer: {content}\n")
    
    return content



if __name__ == "__main__":
    pass