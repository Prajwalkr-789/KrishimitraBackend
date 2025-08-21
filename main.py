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
from agents.DiseaseDetection import handle_user_query_Disease_detector
from flask_cors import CORS
import tempfile
import re
from werkzeug.utils import secure_filename
# Create uploads directory if needed

app = Flask(__name__)
CORS(app , origins=["https://krishimitra-green.vercel.app","http://localhost:3000"] ) 

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# def save_uploaded_file(file_bytes, extension=".jpg"):
#     """Save uploaded file to uploads directory"""
#     filename = f"{uuid.uuid4()}{extension}"
#     filepath = os.path.join(UPLOADS_DIR, filename)
#     with open(filepath, "wb") as f:
#         f.write(file_bytes)
#     return filepath

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


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask app is running on Render!"})


@app.route("/detect_disease", methods=["POST"])
def detect_disease():
    # Get query text
    query = request.form.get("query")
    # Get image file
    image = request.files["image"]

    # Save temporarily
    # image_path = f"./{image.filename}"
    # image.save(image_path)

    filename = secure_filename(image.filename)
    temp_dir = tempfile.mkdtemp()
    image_path = os.path.join(temp_dir, filename)
    image.save(image_path)

    if not filename:
        return jsonify({"error": "No file uploaded"}), 400

    # Create model instance
    state = init_state()
    state["user_query"] = query
    state["image_path"] = image_path
    state["language"] = request.form.get("language", "english").lower()
    try:
        result = handle_user_query_Disease_detector(state["user_query"], state["image_path"], state["language"])
        print("LLM Response:", result)
        if isinstance(result, str):
            result = result.strip()
            result = result.replace("```json", "").replace("```", "").strip()
            result = json.loads(result)
            print("Parsed JSON:", result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    if isinstance(result, str):
        result = result.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        result = json.loads(result) 
    print("LLM Response:", result)
    # result = re.sub(r'\n{2,}', '\n', resul

    return jsonify(result)

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
    app.run(host="0.0.0.0",port = port)  # Set debug=True for development