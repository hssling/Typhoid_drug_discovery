"""
Streamlit Cloud Entry Point
"""
import sys
from pathlib import Path

# Add the scripts directory to path to handle internal imports if any
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR / 'scripts'))

# Import and run the main dashboard logic
# We can either import and call a main() function or just execute the script
with open(BASE_DIR / 'scripts' / 'v4_dashboard_global.py', 'r', encoding='utf-8') as f:
    exec(f.read())
