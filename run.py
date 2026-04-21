"""
Run script for the Intelligence Query Engine API
Use this to start the server locally for testing
"""

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Intelligence Query Engine API")
    print("=" * 60)
    print("\n📋 Available endpoints:")
    print("  GET  /api/profiles              - Query with filters, sorting, pagination")
    print("  GET  /api/profiles/search       - Natural language search")
    print("  GET  /api/profiles/{id}         - Get profile by ID")
    print("  POST /api/profiles              - Create a new profile")
    print("  DELETE /api/profiles/{id}       - Delete a profile")
    print("\n📍 Local URL: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/")
    print("\n📝 Example queries:")
    print("  http://localhost:8000/api/profiles?gender=male&country_id=NG")
    print("  http://localhost:8000/api/profiles/search?q=young males from nigeria")
    print("\n⚠️  Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=True)