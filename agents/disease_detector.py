# agents/disease_detector.py
from services.gemini_vision import analyze_disease_image   # Updated import
from services.disease_db import disease_db
from agents.orchestrator import AgentState

def detect_disease(state: AgentState) -> AgentState:
    if not state.get("image_path"):
        return state
    
    try:
        # First try database match
        match = disease_db.match_image(state["image_path"])
        
        if match:
            return {
                **state,
                "disease_info": {
                    "crop": match.get("crop", "Unknown"),
                    "disease": match["disease"],
                    "source": "database",
                    "confidence": "High",
                    "treatment": "See database recommendations"
                }
            }
        
        # Fallback to Gemini Vision
        analysis = analyze_disease_image(state["image_path"])
        return {
            **state,
            "disease_info": {
                "crop": analysis.get("crop", "Unknown"),
                "disease": analysis.get("disease", "Unknown"),
                "treatment": analysis.get("organic_treatment", "") or analysis.get("treatment", ""),
                "source": "gemini",
                "confidence": analysis.get("confidence", "Medium"),
                "details": analysis  # Store full analysis
            }
        }
    except Exception as e:
        print(f"Disease detection error: {str(e)}")
        return state