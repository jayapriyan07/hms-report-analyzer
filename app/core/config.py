import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Settings:
    """
    Core settings and environment configuration for the HMS backend.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # We can add custom configuration properties here
    PROJECT_NAME: str = "HMS Agentic Medical Report Analysis Backend"

settings = Settings()
