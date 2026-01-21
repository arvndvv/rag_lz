
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath("c:/Users/athul/OneDrive/Desktop/projects/python/rag/common"))

try:
    from functions.query_utils import get_data_using_gemini
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Other error: {e}")
