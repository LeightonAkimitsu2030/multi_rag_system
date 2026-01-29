import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use GOOGLE_API_KEY for Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Vector DB Paths
    AIRLINE_DB_PATH = "data/airline_policy_vectordb"
    STORIES_DB_PATH = "data/stories_vectordb"