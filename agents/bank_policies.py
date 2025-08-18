# services/query_pipeline.py
from services.gemini import get_gemini_response

def generate_response(user_query: str, language: str = "english") -> str:
    """
    Generate a structured agricultural response using AI.
    """
    prompt = f"""You are an expert on agricultural banking policies in India. The user asked: "{user_query}".Return ONLY a JSON array with max 6 objects. Each object must include exactly these keys:name,provider,type,description (max 25 words),interest_rate,loan_amount,eligibility(array of short strings),benefits(array of short strings),source_url (string|null) Use null for unknown values. Keep each array element concise. Prefer authoritative sources but if unknown set source_url to null. Output valid JSON only.Language: {language}"""
    final_response = get_gemini_response(prompt)
    return final_response


def handle_user_query_policies(user_query: str, language: str = "english") -> str:
    final_answer = generate_response(user_query,language)
    print(f"Final Answer: {final_answer}")
    return final_answer