# services/query_pipeline.py
import json
from services.gemini import get_gemini_response
from services.chatgpt import get_chatgpt_response
import time



# Load your JSON database once
try:
    with open(r"E:\CapitalOne\Schemes.json", "r", encoding="utf-8") as f:
        CROPS_DB = json.load(f)
except Exception as e:
    print("Error loading JSON database:", e)
    CROPS_DB = []
    

# -----------------------------
# Step 1: Extract keywords from user query
# -----------------------------



def extract_keywords(user_query: str, language: str = "english") -> list:


    
    prompt = f"""
    Extract the main keywords and key phrases from the following user query. Return only a comma-separated list of keywords, no extra text:

    Query: "{user_query}"
    Language: {language}

    Example Output:
    ["soil type", "temperature", "rainfall"]
    """
    ai_response = get_gemini_response(prompt)
    print(f"AI Response for Keywords: {ai_response}")
    try:
        keywords = [kw.strip() for kw in ai_response.split(",") if kw.strip()]
    except:
        keywords = []
    
    print(f"Extracted Keywords: {keywords}")
    if not keywords:
        print("No keywords extracted, using default keywords.")
        keywords = ["agriculture", "crops", "farming", "soil", "weather"]
    return keywords

# -----------------------------
# Step 2: Search JSON database using keywords
# -----------------------------

def deep_contains(data, keyword: str) -> bool:
    """Recursively search if keyword exists in any value of nested data."""
    if isinstance(data, dict):
        return any(deep_contains(v, keyword) for v in data.values())
    elif isinstance(data, list):
        return any(deep_contains(item, keyword) for item in data)
    else:
        return keyword.lower() in str(data).lower()

def search_db(crops_db: list, keywords: list) -> list:
    results = []
    for entry in crops_db:
        for kw in keywords:
            if deep_contains(entry, kw):
                print(f"Matched entry with keyword: '{kw}'")
                results.append(entry)
                break  # Don't match same entry multiple times
    print(f"Total matched entries: {len(results)}")
    return results





# -----------------------------
# Step 3: Feed DB results + query to AI for final response
# -----------------------------
def generate_response(user_query: str, db_results:str , language: str = "english") -> str:
    """
    Generate a structured agricultural response using AI.
    """
    prompt = f"""You are an agricultural advisor india.the user asked"{user_query}". Language: {language}.Return ONLY JSON. Each object must include:name, department, type, description, benefits, eligibility, website: link of the scheme website.If multiple schemes, return as JSON array. No extra text."""
    final_response = get_gemini_response(prompt)
    return final_response

# -----------------------------
# Step 4: Full pipeline
# -----------------------------
# Start total timer

total_start = time.perf_counter()
def handle_user_query_schemes(user_query: str, language: str = "english") -> str:
    # start = time.perf_counter()
    # keywords = extract_keywords(user_query, language)
    # db_results = search_db(CROPS_DB ,keywords)
    # end = time.perf_counter()
    # print(f"Search completed in {end - start:.4f} seconds. Found {len(db_results)} results.")
    final_answer = generate_response(user_query,language)
    print(f"Final Answer: {final_answer}")
    return final_answer
    


