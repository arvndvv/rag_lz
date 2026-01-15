import sys
import os

# Add current directory to sys.path to allow imports from common
sys.path.append(os.getcwd())

from common.functions.ingestion_utils import load_documents_with_docling_and_gemini

def main():
    data_path = os.path.join(os.getcwd(), "input")
    print(f"Testing image extraction on: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} does not exist.")
        return

    try:
        created_files = load_documents_with_docling_and_gemini(data_path)
        print("\nVerification process completed.")
        print(f"Created {len(created_files)} markdown files:")
        for f in created_files:
            print(f" - {f}")
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    main()
