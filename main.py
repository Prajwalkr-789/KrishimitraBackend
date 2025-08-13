# main.py
from graph import workflow
from agents.orchestrator import AgentState
from datetime import datetime
import json
import os
import uuid

# Create uploads directory if needed
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def save_uploaded_file(file_bytes, extension=".jpg"):
    """Save uploaded file to uploads directory"""
    filename = f"{uuid.uuid4()}{extension}"
    filepath = os.path.join(UPLOADS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return filepath

def main():
    print("=== KrishiMitra Agriculture Advisor ===")
    print("Choose input type:")
    print("1. Text Query")
    print("2. Image Upload")
    choice = input("Enter choice (1/2): ").strip()
    
    # Initialize common state
    state = AgentState(
        user_query=None,
        location=None,
        language="hindi",
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
    
    if choice == "1":
        # Text-based query
        state["user_query"] = input("Enter your agricultural query: ")
        state["location"] = input("Enter your location (e.g. Punjab): ")
        state["language"] = input("Enter language (e.g. hindi, english): ").lower() or "hindi"
        
    elif choice == "2":
        # Image upload
        print("\nSupported formats: JPG, PNG")
        file_path = input("Enter image file path: ").strip()
        
        try:
            # Validate and save file
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            
            extension = os.path.splitext(file_path)[1].lower()
            if extension not in [".jpg", ".jpeg", ".png"]:
                extension = ".jpg"  # Default extension
            
            state["image_path"] = save_uploaded_file(file_bytes, extension)
            state["language"] = input("Enter language for response: ").lower() or "hindi"
            print(f"Image uploaded: {state['image_path']}")
            
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return
    
    else:
        print("Invalid choice")
        return
    
    # Run the workflow
    print("\nProcessing your request...")
    result = workflow.invoke(state)
    
    # Display results
    print("\n=== Final Recommendation ===")
    print(result["llm_response"])
    
    # Show debug info
    if result.get("disease_info"):
        print("\n=== Disease Analysis ===")
        print(json.dumps(result["disease_info"], indent=2))
    
    if result.get("crop_recommendations"):
        print("\n=== Crop Recommendations ===")
        print(json.dumps(result["crop_recommendations"], indent=2))
    
    if result.get("sql_query"):
        print("\n=== Database Query ===")
        print(result["sql_query"])

if __name__ == "__main__":
    main()