# main.py
from flask import Flask, request, jsonify
from graph import workflow
from agents.orchestrator import AgentState
from datetime import datetime
import json
import os
import uuid
from agents.schemes import handle_user_query_schemes
from agents.Market_Prices import fetch_market_prices_full
from agents.bank_policies import handle_user_query_policies
from flask_cors import CORS
import re
# Create uploads directory if needed

app = Flask(__name__)
CORS(app) 

# UPLOADS_DIR = "uploads"
# os.makedirs(UPLOADS_DIR, exist_ok=True)

# def save_uploaded_file(file_bytes, extension=".jpg"):
#     """Save uploaded file to uploads directory"""
#     filename = f"{uuid.uuid4()}{extension}"
#     filepath = os.path.join(UPLOADS_DIR, filename)
#     with open(filepath, "wb") as f:
#         f.write(file_bytes)
#     return filepath

# def main():
    # print("=== KrishiMitra Agriculture Advisor ===")
    # print("Choose input type:")
    # print("1. Text Query")
    # print("2. Image Upload")
    # print("3. Government Schemes Query")
    # choice = input("Enter choice (1/2/3): ").strip()
    
    # Initialize common state
    # state = AgentState(
    #     user_query=None,
    #     location=None,
    #     language="english",
    #     image_path=None,
    #     timestamp=datetime.now().isoformat(),
    #     soil_ph=None,
    #     rainfall=None,
    #     temperature=None,
    #     soil_type=None,
    #     altitude=None,
    #     season=None,
    #     sql_query="",
    #     crop_recommendations=[],
    #     disease_info=None,
    #     llm_response=""
    # )
    
#     if choice == "1":
#         # Text-based query
#         state["user_query"] = input("Enter your agricultural query: ")
#         state["location"] = input("Enter your location (e.g. Punjab): ")
#         state["language"] = input("Enter language (e.g. hindi, english): ").lower() or "hindi"
        
#     elif choice == "2":
#         # Image upload
#         print("\nSupported formats: JPG, PNG")
#         file_path = input("Enter image file path: ").strip()
        
#         try:
#             # Validate and save file
#             with open(file_path, "rb") as f:
#                 file_bytes = f.read()
            
#             extension = os.path.splitext(file_path)[1].lower()
#             if extension not in [".jpg", ".jpeg", ".png"]:
#                 extension = ".jpg"  # Default extension
            
#             state["image_path"] = save_uploaded_file(file_bytes, extension)
#             state["language"] = input("Enter language for response: ").lower() or "hindi"
#             print(f"Image uploaded: {state['image_path']}")
            
#         except Exception as e:
#             print(f"Error uploading image: {str(e)}")
#             return
        
#     elif choice == "3":
#         state["user_query"] = input("Enter scheme-related query: ")
#         state["language"] = input("Enter language for response: ").lower() or "hindi"
#         print("\nFetching relevant government schemes...")
#         result = handle_user_query_schemes(state)
#     elif choice == "4":
#         # state["user_query"] = input("Enter scheme-related query: ")
#         # state["language"] = input("Enter language for response: ").lower() or "hindi"
#         print("\nFetching relevant government schemes...")
#         all_prices = fetch_market_prices_full()
#         for row in all_prices:
#             print(row)
#     else:
#         print("Invalid choice")
#         return
    
#     # Run the workflow
#     print("\nProcessing your request...")
#     # result = workflow.invoke(state)
    
#     # Display results
#     print("\n=== Final Recommendation ===")
#     print(result["llm_response"])
    
#     # Show debug info
#     if result.get("disease_info"):
#         print("\n=== Disease Analysis ===")
#         print(json.dumps(result["disease_info"], indent=2))
    
#     if result.get("crop_recommendations"):
#         print("\n=== Crop Recommendations ===")
#         print(json.dumps(result["crop_recommendations"], indent=2))
    
#     if result.get("sql_query"):
#         print("\n=== Database Query ===")
#         print(result["sql_query"])

# if __name__ == "__main__":
#     main()

def init_state():
    """Initialize AgentState"""
    return AgentState(
        user_query=None,
        location=None,
        language="english",
        image_path=None,
        timestamp=datetime.now().isoformat(),
        soil_ph=None,
        rainfall=None,
        temperature=None,
        soil_type=None,
        altitude=None,
        season=None,
        sql_query="",
        crop_recommendations=[],
        disease_info=None,
        llm_response=""
    )


@app.route("/ask", methods=["POST"])
def ask():
    # Get data from frontend
    data = request.json
    state = init_state()
    state["user_query"] = data.get("text")           # text query from frontend
    state["location"] = data.get("location")
    state["language"] = data.get("language", "english").lower()

    # Call your workflow or any processing function
    result = workflow.invoke(state)
    print("LLM Response:", result)
    # result = re.sub(r'\n{2,}', '\n', result)

    return result

@app.route("/bank_policies", methods=["POST"])
def bank_policies():
    # Get data from frontend
    data = request.json
    state = init_state()
    state["user_query"] = data.get("query")           # text query from frontend
    state["language"] = data.get("language", "english").lower()

    # Call your workflow or any processing function
    result = handle_user_query_policies(state["user_query"], state["language"])
    if result.startswith("```json"):
        result = result[7:]  # skip ```json
    if result.endswith("```"):
        result = result[:-3]
    result = result.strip()

    print("LLM Response:", result)
    # result = re.sub(r'\n{2,}', '\n', result

    return result

@app.route("/market_price", methods=["POST"])
def market_price():
    # Get data from frontend
    # data = request.json
    # state = init_state()

    result = fetch_market_prices_full()
    return result


@app.route("/schemes_query", methods=["POST"])
def text_query():
    # Get data from frontend
    data = request.json

    # Initialize state
    state = init_state()
    state["user_query"] = data.get("query")           # text query from frontend
    # state["location"] = data.get("location")         # location from frontend
    state["language"] = data.get("language", "hindi").lower()  # optional, default "hindi"

    # Call your workflow or any processing function
    # result = workflow.invoke(state)
    result = handle_user_query_schemes(state)
    if isinstance(result, str):
        result = result.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        result = json.loads(result) 

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0",port = port)