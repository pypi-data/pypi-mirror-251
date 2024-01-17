import os
from dotenv import load_dotenv

class MissingEnvironmentVariablesError(Exception):
    """Exception raised when required environment variables are missing."""

def initialize_environment(required_vars):
    load_dotenv()
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise MissingEnvironmentVariablesError(f"Missing required environment variables: {', '.join(missing_vars)}")
