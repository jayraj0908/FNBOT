"""
Test script for Trust Bodhi Backend
"""

import requests
import json

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_api_documentation():
    """Test if API documentation is accessible"""
    try:
        response = requests.get('http://localhost:8000/docs')
        if response.status_code == 200:
            print("✅ API documentation accessible")
            return True
        else:
            print(f"❌ API documentation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API documentation error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Trust Bodhi Backend...")
    print("=" * 50)
    
    # Test health check
    health_ok = test_health_check()
    
    # Test API documentation
    docs_ok = test_api_documentation()
    
    print("=" * 50)
    if health_ok and docs_ok:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the backend server.")
    
    print("\n📋 Available endpoints:")
    print("- GET  /health - Health check")
    print("- POST /analyze - BBB file processing")
    print("- POST /analyze-nectar - Nectar file processing")
    print("- GET  /files/{filename} - File download")
    print("- GET  /docs - API documentation") 