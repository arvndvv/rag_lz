from functions.query_utils import (
    load_bm25_chunks,
    get_bm25_results,
    get_vector_results,
    merge_and_deduplicate,
    rerank_documents,
    generate_answer
)
from functions.make_section import CV_HEADING_PATTERNS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from config import MODEL_NAME
import json

def get_section_using_llm(question):
    TEMPLATE = """
    You are an expert CV analyzer.

    Your task is to determine which CV section(s) are most relevant to answer a given user question.

    Available CV sections:
    - summary
    - skills
    - experience
    - education
    - projects
    - certifications
    - achievements
    - interests
    - languages
    - publications
    - references
    - personal
    - general

    Rules:
    1. Choose the MOST RELEVANT section(s).
    2. You may return multiple sections if needed.
    3. Do NOT invent new sections.
    4. Prefer:
    - "skills" → technologies, tools, programming languages
    - "experience" → worked at, employed, job history
    - "projects" → built, developed, implemented, worked on a product
    - "interests" → sports, hobbies, extracurricular activities
    5. Output ONLY valid JSON.
    6. If no section is relevant, return "general" section.

    Return format:
    {{
    "sections": ["section1", "section2"],
    "confidence": "high | medium | low",
    "reason": "short explanation"
    }}

    Input question:

    {question}
    """
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    model = ChatOllama(model=MODEL_NAME, format="json")
    chain = prompt | model
    response = chain.invoke({"question": question})
    content = response.content
    cleaned_content = content.strip()
    try:
        json_data = json.loads(cleaned_content)
        print(json_data)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON {e}")

def query_rag(query_text):
    """Main RAG pipeline."""
    # 1. BM25 Retrieval
    # chunks = load_bm25_chunks()
    # if chunks is None: return
    # bm25_docs = get_bm25_results(chunks, query_text)
    # bm25_docs = []
    
    # 2. Vector Retrieval
    section=get_section_using_llm(query_text)
    vector_docs = get_vector_results(query_text,section["sections"])
    
    # 3. Merge & Deduplicate
    # merged_docs = merge_and_deduplicate(bm25_docs, vector_docs)
    merged_docs = vector_docs
    
    if not merged_docs:
        print("No relevant documents found.")
        return

    # 4. Rerank
    # top_docs = rerank_documents(query_text, merged_docs)
    top_docs = merged_docs
    
    # 5. Generate Answer
    answer = generate_answer(query_text, top_docs)
    
    print(answer)
    print("\nSources:")
    for doc in top_docs:
        print(f"- {doc.metadata.get('source', 'Unknown')}")

def main():
    query_text = "Which candidates show an interest in sports can develop a android app"
    query_rag(query_text)
    

if __name__ == "__main__":
    main()
