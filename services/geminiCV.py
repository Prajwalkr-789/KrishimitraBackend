# services/gemini.py
import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv
# from google.generativeai import HarmCategory, HarmBlockThreshold # type: ignore

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response_cv(prompt: str,image_path:str ,temperature: float = 0.3  ) -> str:
    """Get response from Gemini with safety settings"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    response = model.generate_content(
        [
            prompt,
            {"mime_type": "image/jpeg", "data": open(image_path, "rb").read()}
        ],
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 4000,
        },
        # safety_settings={
        #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        # },
        stream=True
    )
    
    # Collect all chunks
    full_response = []
    for chunk in response:
        if hasattr(chunk, 'text') and chunk.text:
            full_response.append(chunk.text)
    
    return "".join(full_response)