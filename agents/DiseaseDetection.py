# services/query_pipeline.py
from services.geminiCV import get_gemini_response_cv

def generate_response(user_query: str , image_path , language: str = "english") -> str:
    """
    Generate a structured agricultural response using AI.
    """
    prompt = f"""You are an expert agricultural crop disease detector. Analyze the uploaded image and the user query: "{user_query}". Return a JSON object with keys: disease_name,symptoms,cause,recommended_treatment,preventive_measures,source_url (string|null). Respond only as a valid JSON object. Language: {language}"""
    final_response = get_gemini_response_cv(prompt , image_path=image_path)
    return final_response


def handle_user_query_Disease_detector(user_query: str,image_path , language: str = "english") -> str:
    final_answer = generate_response(user_query,image_path, language)
    print(f"Final Answer: {final_answer}")
    return final_answer