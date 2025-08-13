# agents/orchestrator.py
from typing import TypedDict, List, Dict, Optional, Union

class AgentState(TypedDict):
    # User inputs
    user_query: Optional[str]
    location: Optional[str]
    language: Optional[str]
    image_path: Optional[str]  # New field for image uploads
    timestamp: str
    
    # Extracted parameters
    soil_ph: Optional[float]
    rainfall: Optional[float]
    temperature: Optional[float]
    soil_type: Optional[str]
    altitude: Optional[float]
    season: Optional[str]
    
    # Agent outputs
    sql_query: str
    crop_recommendations: List[Dict]
    disease_info: Optional[Dict]  # New field for disease results
    llm_response: str