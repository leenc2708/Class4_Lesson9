#!/usr/bin/env python3
"""
Launch script for Streamlit app with WSL2-compatible settings.
This script handles TTY issues that commonly occur in WSL2 environments.
"""

import os
import sys
import subprocess
from pathlib import Path

def set_environment_variables():
    """Set environment variables to handle TTY issues in WSL2."""
    env_vars = {
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'STREAMLIT_SERVER_RUN_ON_SAVE': 'false',
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_SERVER_ENABLE_CORS': 'false',
        'STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION': 'false',
        'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
        'STREAMLIT_LOGGER_LEVEL': 'info',
        'STREAMLIT_CLIENT_SHOW_ERROR_DETAILS': 'false',
        'PYTHONUNBUFFERED': '1',
        'PYTHONDONTWRITEBYTECODE': '1',
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value

def main():
    """Main function to launch Streamlit with proper settings."""
    print("Setting up WSL2-compatible environment...")
    set_environment_variables()
    
    # Check if main.py exists
    main_py = Path("main.py")
    if not main_py.exists():
        print("Error: main.py not found in current directory")
        sys.exit(1)
    
    print("Starting Streamlit with WSL2-compatible settings...")
    print("Access the app at: http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # We're in a virtual environment, use streamlit directly
            subprocess.run(["streamlit", "run", "main.py"], check=True)
        else:
            # Use python -m streamlit
            subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()
