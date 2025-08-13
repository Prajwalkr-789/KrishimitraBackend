# agents/param_extractor.py
from services.gemini import get_gemini_response 
from utils.helpers import get_current_season
from agents.orchestrator import AgentState
import json

def extract_parameters(state: AgentState) -> AgentState:
    """Extract agricultural parameters from natural language query"""
    prompt = f"""
    Extract agricultural parameters from the user query below.
    Return ONLY as JSON with these keys: 
    "soil_ph", "rainfall", "temperature", "soil_type", "altitude"
    
    If a parameter isn't mentioned, use null.
    Respond in the user's language: {state['language']}
    
    Query: {state['user_query']}
    
    Example Output: {{
        "soil_ph": 6.2, 
        "rainfall": 800, 
        "temperature": 22, 
        "soil_type": "Loam",
        "altitude": 300
    }}
    """
    
    response = get_gemini_response(prompt)
    
    try:
        params = json.loads(response)
    except:
        params = {
            "soil_ph": None,
            "rainfall": None,
            "temperature": None,
            "soil_type": None,
            "altitude": None
        }
    
    return {
        **state,
        "soil_ph": params.get("soil_ph"),
        "rainfall": params.get("rainfall"),
        "temperature": params.get("temperature"),
        "soil_type": params.get("soil_type"),
        "altitude": params.get("altitude"),
        "season": get_current_season()
    }