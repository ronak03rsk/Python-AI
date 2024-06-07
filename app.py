import os
import json
from pathlib import Path
from zipfile import ZipFile
import requests
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("API key is not set in environment variables")

# Function to get user input for the type of application
def get_user_input():
    app_type = input("Enter the type of application you want to build (e.g., web app for to-do list): ")
    return app_type

# Function to call the AI API and get file structure
def get_file_structure(prompt):
    # Example API call to Gemini or similar free AI API
    api_url = "https://ai.google.dev/api/rest/v1beta/files#resource:-file"  # Placeholder URL, replace with actual API endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",  # Use the API key from the environment
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
    
    try:
        return response.json()  # Expecting JSON response with file structure
    except json.JSONDecodeError:
        print("Failed to decode JSON response")
        return None

# Function to generate files based on the AI's response
def create_files(file_structure):
    base_dir = Path("generated_application")
    base_dir.mkdir(exist_ok=True)
    
    for file_info in file_structure:
        file_path = base_dir / file_info["name"]
        file_content = file_info["content"]
        
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directories exist
        with open(file_path, "w") as file:
            file.write(file_content)  # Write file content

# Function to zip the generated files
def zip_files(directory):
    zip_name = "generated_application.zip"
    with ZipFile(zip_name, 'w') as zipf:
        for file in Path(directory).rglob('*'):
            zipf.write(file, file.relative_to(directory))
    print(f"Files are zipped as {zip_name}")

# Main function to execute the steps
def main():
    # Step 1: Get user input
    print("Welcome to the AI application generator!")
    prompt = get_user_input()
    
    # Step 2: Get file structure from AI API
    file_structure = get_file_structure(prompt)
    if not file_structure:
        print("Failed to get a valid file structure from the AI API")
        return
    
    # Step 3: Create files based on the file structure
    try:
        create_files(file_structure)
    except Exception as e:
        print(f"Failed to create files: {e}")
        return
    
    # Step 4: Zip the generated files
    zip_files("generated_application")
    
    # Optionally, Step 5: Add basic validation or testing here
    # Example: We could validate file types or check if a main entry point file exists

if __name__ == "__main__":
    main()
