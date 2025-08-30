# WSL2 Streamlit TTY Fix

This document explains the fix for the "tcgetpgrp failed: Not a tty" error that occurs when running Streamlit in WSL2 environments.

## Problem

The error "tcgetpgrp failed: Not a tty" occurs when Streamlit tries to access terminal properties in WSL2 environments where there's no proper terminal (TTY) available.

## Solution

The fix includes:

1. **Updated Streamlit Configuration** (`.streamlit/config.toml`)
   - Added comprehensive server settings
   - Disabled features that require TTY access
   - Set proper headless mode configuration

2. **Launch Scripts**
   - `run_streamlit.sh` - Bash script with environment variables
   - `run_streamlit.py` - Python script with environment variables

## Usage

### Option 1: Use the Bash Script (Recommended)
```bash
./run_streamlit.sh
```

### Option 2: Use the Python Script
```bash
./run_streamlit.py
```

### Option 3: Direct Command with Environment Variables
```bash
STREAMLIT_SERVER_HEADLESS=true STREAMLIT_SERVER_RUN_ON_SAVE=false streamlit run main.py
```

## Configuration Details

The following environment variables are set to handle TTY issues:

- `STREAMLIT_SERVER_HEADLESS=true` - Runs in headless mode
- `STREAMLIT_SERVER_RUN_ON_SAVE=false` - Disables auto-reload on save
- `STREAMLIT_SERVER_PORT=8501` - Sets port to 8501
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0` - Binds to all interfaces
- `PYTHONUNBUFFERED=1` - Prevents output buffering
- `PYTHONDONTWRITEBYTECODE=1` - Prevents .pyc file creation

## Access the Application

After running any of the launch methods, access the application at:
- **Local**: http://localhost:8501
- **Network**: http://[your-wsl2-ip]:8501

## Troubleshooting

If you still encounter issues:

1. **Check WSL2 Terminal**: Ensure you're running in a proper WSL2 terminal
2. **Update Dependencies**: Run `pip install -r requirements.txt`
3. **Check Port Availability**: Ensure port 8501 is not in use
4. **Firewall Settings**: Check Windows firewall settings for WSL2

## Files Modified/Created

- `.streamlit/config.toml` - Updated with WSL2-compatible settings
- `run_streamlit.sh` - Bash launch script
- `run_streamlit.py` - Python launch script
- `README_WSL2_FIX.md` - This documentation file
