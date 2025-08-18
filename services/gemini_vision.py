# services/gemini_vision.py
import google.generativeai as genai #type: ignore
import os
import json
from dotenv import load_dotenv
# from google.generativeai.types import HarmCategory, HarmBlockThreshold # type: ignore

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_disease_image(image_path: str) -> dict:
    """Analyze crop disease image using Gemini Pro Vision"""
    try:
        # Initialize the vision model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Create the prompt
        prompt = """
        You are an agricultural expert analyzing a crop disease image. Provide:
        1. Crop type
        2. Disease name (be specific)
        3. Confidence level (Low, Medium, High)
        4. Symptoms description
        5. Organic treatment
        6. Chemical treatment (if severe)
        7. Prevention methods
        
        Respond in JSON format only with these keys:
        {
            "crop": "",
            "disease": "",
            "confidence": "",
            "symptoms": "",
            "organic_treatment": "",
            "chemical_treatment": "",
            "prevention": ""
        }
        """
        
        # Read image file
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Generate content
        response = model.generate_content(
            [prompt, {"mime_type": "image/jpeg", "data": image_data}],
            # safety_settings={
            #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            # }
        )
        
        # Extract JSON from response
        return extract_json(response.text)
    
    except Exception as e:
        print(f"Gemini Vision error: {str(e)}")
        return {
            "crop": "Unknown",
            "disease": "Analysis Failed",
            "confidence": "Low",
            "symptoms": "",
            "organic_treatment": "Please consult a local agriculture expert",
            "chemical_treatment": "",
            "prevention": ""
        }

def extract_json(text: str) -> dict:
    """Extract JSON from Gemini's response"""
    try:
        # Find JSON substring
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        
        # Clean and parse
        json_str = json_str.replace('```json', '').replace('```', '').strip()
        return json.loads(json_str)
    except:
        return {
            "error": "Failed to parse response",
            "raw_output": text
        }