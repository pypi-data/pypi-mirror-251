import os
import sys
from dotenv import load_dotenv
from typing import List

def is_env_var_present(var_name: str):
    """Check if a required environment variable is set."""
    value = os.getenv(var_name)
    if value is None:
        sys.exit(f"Error: Required environment variable '{var_name}' is not set.")

def initialize_environment(required_vars: List[str]) -> None:
    """Load environment variables and check if required vars are present."""
    load_dotenv()
    for var in required_vars:
        is_env_var_present(var)