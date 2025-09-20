#!/usr/bin/env python3
"""
VTOL Medical Drone System - Server Startup Script
Easy way to start the Flask server with proper configuration
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import pandas
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def start_server():
    """Start the Flask server"""
    print("🚁 VTOL Medical Drone System - Starting Server...")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {script_dir}")
    print("🌐 Starting Flask server on http://localhost:8080")
    print("📡 API endpoints available at http://localhost:8080/api/")
    print("🔧 Real-time updates enabled")
    print("=" * 60)
    
    try:
        # Import and run the server
        from server import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8080')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the server
        app.run(debug=True, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main function"""
    print("🚁 VTOL Medical Drone System")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install_dependencies()
        return
    
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("python start_server.py --install")
        return
    
    start_server()

if __name__ == "__main__":
    main()
