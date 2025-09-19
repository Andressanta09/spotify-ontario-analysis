#!/usr/bin/env python3
"""
Startup script for Ontario Music Analysis Dashboard
Uses environment variables for configuration
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    """Main startup function"""
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    dashboard_port = os.getenv("DASHBOARD_PORT", "8501")
    dashboard_title = os.getenv("DASHBOARD_TITLE", "Ontario Music Analysis")
    
    print(f"🎵 Starting {dashboard_title}")
    print(f"🌐 Port: {dashboard_port}")
    print(f"📁 Dashboard directory: {os.getcwd()}")
    
    # Check if data.json exists
    if not os.path.exists("data.json"):
        print("⚠️  Warning: data.json not found!")
        print("📝 Please run the analysis notebooks first:")
        print("   1. notebooks/01_collect.ipynb")
        print("   2. notebooks/02_clean.ipynb") 
        print("   3. notebooks/03_analysis.ipynb")
        print()
        
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Startup cancelled")
            return
    
    # Start Streamlit
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", dashboard_port,
            "--server.headless", "true"
        ]
        
        print(f"🚀 Launching dashboard...")
        print(f"🔗 Open: http://localhost:{dashboard_port}")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

if __name__ == "__main__":
    main()