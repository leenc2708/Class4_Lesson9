#!/bin/bash

# Set environment variables to handle TTY issues in WSL2
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_RUN_ON_SAVE=false
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_LOGGER_LEVEL=info
export STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false

# Suppress TTY-related warnings
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Run Streamlit with proper environment
streamlit run main.py

echo "Starting Streamlit with WSL2-compatible settings..."
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"

