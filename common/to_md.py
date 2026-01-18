import os
from config import DATA_PATH, DB_PATH, EMBEDDING_MODEL_NAME, COLLECTION_NAME
from functions.ingestion_utils import (
    load_documents,
    load_documents_with_docling,
    load_documents_with_markitdown,
    load_documents_with_docling_tesseract
)
from functions.marker_utils import load_documents_with_marker

is_markdown = True
should_owerwrite=False
folder_to_save="md" if is_markdown else "json"
extension="md" if is_markdown else "json"
def skip_condition_func(file_name):
    if should_owerwrite:
        return False
    output_path = os.path.join("processed",folder_to_save, file_name + "."+extension)

    return os.path.exists(output_path)

def makeMd():
    # documents = load_documents_with_docling(DATA_PATH,is_markdown)
    documents = load_documents_with_marker(DATA_PATH,is_markdown,skip_condition_func)
    if not os.path.exists("processed"):
        os.makedirs("processed")

    try:
        for doc in documents:
            # Using Docling's markdown output (stored in page_content)
            file_name = os.path.basename(doc.metadata["source"]) if is_markdown else os.path.basename(doc["metadata"]["source"])
            output_path = os.path.join("processed",folder_to_save, file_name + "."+extension)
            with open(output_path, 'w', encoding='utf-8') as f:
                if is_markdown:
                    f.write(doc.page_content)
                else:
                    import json
                    f.write(json.dumps(doc["page_content"]))
    except Exception as e:
        print("is_markdown ",is_markdown, "is it correct")
        print(f"Error converting {filename}: {e}")
        print("is_markdown ",is_markdown, "is it correct")

if __name__ == "__main__":
    print("md converting")
    makeMd()