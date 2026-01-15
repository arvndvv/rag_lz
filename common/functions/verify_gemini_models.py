
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")
if not api_key:
    print("GEMINI_KEY not found.")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    print("Listing available models...")
    # The method to list models might vary slightly depending on exact SDK version, 
    # but client.models.list() is standard in the new SDK.
    for model in client.models.list():
        print(f"Model: {model.name}")
        # print(f"  Supported methods: {model.supported_generation_methods}")

except Exception as e:
    print(f"Error listing models: {e}")

try:
    print("\nTrying generate_content with 'gemini-1.5-flash'...")
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Hello'
    )
    print("Success with gemini-1.5-flash")
except Exception as e:
    print(f"Failed with gemini-1.5-flash: {e}")

try:
    print("\nTrying generate_content with 'gemini-1.5-flash-001'...")
    response = client.models.generate_content(
        model='gemini-1.5-flash-001',
        contents='Hello'
    )
    print("Success with gemini-1.5-flash-001")
except Exception as e:
    print(f"Failed with gemini-1.5-flash-001: {e}")
