# agents/param_extractor.py
from services.gemini import get_gemini_response 
from utils.helpers import get_current_season
from agents.orchestrator import AgentState
import json
import asyncio

    

def extract_parameters(state: AgentState) -> AgentState:
    prompt = f"""
    Extract the following agricultural parameters from the query:soil_ph, rainfall, temperature, soil_type, altitude.If any are missing, set them to null. Return ONLY a JSON object.Language: {state['language']}Query: {state['user_query']}(e.g. {{"soil_ph": 6.2,"" }}"""
    
    # response = "get_gemini_response(prompt)"
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


