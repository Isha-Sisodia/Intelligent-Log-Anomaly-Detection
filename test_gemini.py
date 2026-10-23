import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send our first request
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain what a log file is in one simple sentence."
)

print(response.text)