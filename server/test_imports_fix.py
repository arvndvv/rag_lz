import sys
import os

# Ensure we can import from common
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
common_dir = os.path.join(project_root, 'common')
sys.path.append(project_root)
sys.path.append(common_dir)

try:
    import functions.database_utils as db_utils
    from config import DB_NAME
    print("Imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
