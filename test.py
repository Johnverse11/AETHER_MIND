import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('C:/Users/JOHN PAUL/Desktop/AETHER_MIND/.env')

# Print the API key
print(f"System GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")
