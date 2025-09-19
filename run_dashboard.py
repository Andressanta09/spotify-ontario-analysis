#!/usr/bin/env python3
"""
Spotify Ontario Analysis Dashboard Launcher

This script launches the Streamlit dashboard with proper configuration.
Run this from the project root directory.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_data():
    """Check if processed data exists."""
    data_dir = Path("data/processed")
    
    if not data_dir.exists():
        print("❌ No processed data directory found.")
        print("🔧 Please run the data collection and cleaning notebooks first:")
        print("   1. notebooks/01_collect.ipynb")
        print("   2. notebooks/02_clean.ipynb")
        return False
    
    # Look for any processed files
    csv_files = list(data_dir.glob("clean_tracks_*.csv"))
    parquet_files = list(data_dir.glob("clean_tracks_*.parquet"))
    
    if not csv_files and not parquet_files:
        print("❌ No processed track data found.")
        print("🔧 Please run the data collection and cleaning notebooks first:")
        print("   1. notebooks/01_collect.ipynb") 
        print("   2. notebooks/02_clean.ipynb")
        return False
    
    print(f"✅ Found {len(csv_files + parquet_files)} processed data file(s)")
    return True

def launch_dashboard():
    """Launch the Streamlit dashboard."""
    dashboard_path = Path("dashboard/app.py")
    
    if not dashboard_path.exists():
        print("❌ Dashboard app.py not found!")
        return False
    
    print("🚀 Launching Spotify Ontario Analysis Dashboard...")
    print("📱 Dashboard will open in your default browser")
    print("🛑 Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main launcher function."""
    print("🎵 Spotify Ontario Analysis Dashboard Launcher")
    print("=" * 50)
    
    # Check current directory
    if not Path("dashboard").exists():
        print("❌ Please run this script from the project root directory")
        print("🔧 Expected structure:")
        print("   project-root/")
        print("   ├── dashboard/")
        print("   ├── data/")
        print("   └── notebooks/")
        sys.exit(1)
    
    # Check requirements
    print("🔍 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    # Check data
    print("📊 Checking processed data...")
    if not check_data():
        sys.exit(1)
    
    # Launch dashboard
    success = launch_dashboard()
    
    if success:
        print("✅ Dashboard session completed successfully")
    else:
        print("❌ Dashboard launch failed")
        sys.exit(1)

if __name__ == "__main__":
    main()