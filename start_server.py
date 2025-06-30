#!/usr/bin/env python3
"""
Startup script for Trust Bodhi Backend
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create necessary directories
    os.makedirs("files", exist_ok=True)
    
    print("🚀 Starting Trust Bodhi Backend...")
    print("📁 Working directory:", os.getcwd())
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,  # Enable auto-reload for development
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 