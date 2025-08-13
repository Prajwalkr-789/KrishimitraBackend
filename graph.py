# graph.py
from langgraph.graph import StateGraph, END
from agents.orchestrator import AgentState
from agents import param_extractor, crop_recommender, response_generator, disease_detector

def create_workflow():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("route_inputs", route_inputs)
    workflow.add_node("param_extractor", param_extractor.extract_parameters)
    workflow.add_node("crop_recommender", crop_recommender.recommend_crops)
    workflow.add_node("disease_detector", disease_detector.detect_disease)
    workflow.add_node("response_generator", response_generator.generate_response)
    
    # Set entry point
    workflow.set_entry_point("route_inputs")
    
    # Define edges
    workflow.add_conditional_edges(
        "route_inputs",
        decide_next,
        {
            "disease_detection": "disease_detector",
            "crop_recommendation": "param_extractor"
        }
    )
    workflow.add_edge("disease_detector", "response_generator")
    workflow.add_edge("param_extractor", "crop_recommender")
    workflow.add_edge("crop_recommender", "response_generator")
    workflow.add_edge("response_generator", END)
    
    return workflow.compile()

def route_inputs(state: AgentState) -> AgentState:
    """Initial routing doesn't modify state"""
    return state

def decide_next(state: AgentState) -> str:
    """Decide whether to run disease detection or crop recommendation"""
    if state.get("image_path"):
        return "disease_detection"
    return "crop_recommendation"

# Compile workflow
workflow = create_workflow()