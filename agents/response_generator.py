# agents/response_generator.py
from services.gemini import get_gemini_response  # Direct import
from agents.orchestrator import AgentState

def generate_response(state: AgentState) -> AgentState:
    # Initialize response components
    crop_response = ""
    disease_response = ""
    
    # Generate crop recommendation response if available
    if state.get("crop_recommendations"):
        crop_list = "\n".join(
            f"- {crop['name']} ({crop['sci_name']})" 
            for crop in state["crop_recommendations"]
        )
        
        crop_prompt = f"""
        You are an agricultural advisor in {state.get('location', 'India')}. 
        Recommend crops based on these parameters:
        - Soil pH: {state.get('soil_ph', 'Not specified')}
        - Rainfall: {state.get('rainfall', 'Not specified')} mm
        - Temperature: {state.get('temperature', 'Not specified')}°C
        - Soil Type: {state.get('soil_type', 'Not specified')}
        - Season: {state.get('season', 'Not specified')}
        
        Recommended crops:
        {crop_list}
        
        Provide planting tips in {state.get('language', 'english')}.
        """
        crop_response = get_gemini_response(crop_prompt)
    
    # Generate disease response if available
    if state.get("disease_info"):
        disease_info = state["disease_info"]
        
        if disease_info["source"] == "database":
            disease_prompt = f"""
            Explain this crop disease in simple {state.get('language', 'english')}:
            - Crop: {disease_info.get('crop', 'Unknown')}
            - Disease: {disease_info['disease']}
            
            Provide:
            1. Symptoms
            2. Organic treatment
            3. Prevention methods
            """
            disease_response = get_gemini_response(disease_prompt)
            
        else:  # Gemini vision response
            disease_response = (
                f"Crop: {disease_info.get('crop', 'Unknown')}\n"
                f"Disease: {disease_info.get('disease', 'Unknown')}\n"
                f"Confidence: {disease_info.get('confidence', 'Medium')}\n\n"
                f"Treatment: {disease_info.get('treatment', '')}\n"
                f"Prevention: {disease_info.get('details', {}).get('prevention', '')}"
            )
    
    # Combine responses
    full_response = f"{crop_response}\n\n{disease_response}".strip()
    return {**state, "llm_response": full_response}