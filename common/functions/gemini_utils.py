import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from PIL import Image

def analyze_image_with_gemini(image: Image.Image, prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Analyzes an image using the Gemini API.
    
    Args:
        image (PIL.Image.Image): The image to analyze.
        prompt (str): The prompt/question about the image.
        model_name (str): The model to use. Defaults to "gemini-2.0-flash".
        
    Returns:
        str: The analysis text from the API.
    """
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        raise ValueError("GEMINI_KEY not found in environment variables.")
    
    client = genai.Client(api_key=api_key)
    
    try:
        from google.genai import types
        import io
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        # default to PNG if format is not available
        fmt = image.format if image.format else 'PNG'
        image.save(img_byte_arr, format=fmt)
        img_byte_arr = img_byte_arr.getvalue()

        response = client.models.generate_content(
            model=model_name,
            contents=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(data=img_byte_arr, mime_type=f"image/{fmt.lower()}")
            ]
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for image analysis: {e}")
        return ""

def get_gemini_response(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Calls the Gemini API with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the API.
        model_name (str): The model to use. Defaults to "gemini-2.0-flash".
        
    Returns:
        str: The text response from the API.
    """
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        raise ValueError("GEMINI_KEY not found in environment variables.")
    
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Log the error or handle it as appropriate for the application
        print(f"Error calling Gemini API: {e}")
        return ""


if __name__ == "__main__":
    response = get_gemini_response("Hello, tell me a joke.")
    print(response)
