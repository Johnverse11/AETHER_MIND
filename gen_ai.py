import google.generativeai as genai
import os

# Set up the Gemini API key environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyA75DeDof3uXHWrcVlD9Zvt3rAVv16K3H4"

def gemini_response(user_input):
    # Retrieve the API key from the environment
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Configure the API with the key
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Define the model to use
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content based on the user input
    response = model.generate_content(user_input)
    
    response_text = response.text

    return {"response": response_text}

