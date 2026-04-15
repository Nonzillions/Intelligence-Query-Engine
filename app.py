from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timezone
import database

# Set up the database
database.create_tables()

# Create the web app
app = Flask(__name__)
CORS(app)  # This allows anyone to call your API

# Helper function: convert age to age group
def get_age_group(age):
    if age is None:
        return None
    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    else:
        return "senior"

# Homepage - tells people your API is working
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Profile Intelligence Service API is running",
        "endpoints": {
            "POST /api/profiles": "Create a profile from a name",
            "GET /api/profiles/{id}": "Get profile by ID",
            "GET /api/profiles": "List all profiles (filters: gender, country_id, age_group)",
            "DELETE /api/profiles/{id}": "Delete a profile"
        }
    })

# CREATE a profile (POST /api/profiles)
@app.route('/api/profiles', methods=['POST', 'OPTIONS'])
def create_profile():
    # Handle pre-flight CORS request
    if request.method == 'OPTIONS':
        return '', 200
    
    # Get the name from the request
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Missing request body"}), 400
    
    name = data.get('name')
    
    # Validate the name
    if not name or name.strip() == "":
        return jsonify({"status": "error", "message": "Missing or empty name"}), 400
    
    if not isinstance(name, str):
        return jsonify({"status": "error", "message": "name is not a string"}), 422
    
    name = name.strip().lower()
    
    try:
        # Call Genderize API
        g = requests.get(f"https://api.genderize.io/?name={name}", timeout=10)
        gd = g.json()
        if gd.get('gender') is None or gd.get('count', 0) == 0:
            return jsonify({"status": "error", "message": "Genderize returned an invalid response"}), 502
        
        # Call Agify API
        a = requests.get(f"https://api.agify.io/?name={name}", timeout=10)
        ad = a.json()
        if ad.get('age') is None:
            return jsonify({"status": "error", "message": "Agify returned an invalid response"}), 502
        
        # Call Nationalize API
        n = requests.get(f"https://api.nationalize.io/?name={name}", timeout=10)
        nd = n.json()
        if not nd.get('country') or len(nd['country']) == 0:
            return jsonify({"status": "error", "message": "Nationalize returned an invalid response"}), 502
        
        # Get the country with highest probability
        top = nd['country'][0]
        
        # Build the profile object
        profile = {
            'id': database.generate_uuid_v7(),
            'name': name,
            'gender': gd['gender'],
            'gender_probability': gd['probability'],
            'sample_size': gd['count'],
            'age': ad['age'],
            'age_group': get_age_group(ad['age']),
            'country_id': top['country_id'],
            'country_probability': top['probability'],
            'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        
        # Save to database (checks for duplicates automatically)
        saved, exists = database.save_profile(profile)
        
        if exists:
            return jsonify({"status": "success", "message": "Profile already exists", "data": saved}), 200
        else:
            return jsonify({"status": "success", "data": saved}), 201
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# READ a profile by ID (GET /api/profiles/{id})
@app.route('/api/profiles/<profile_id>', methods=['GET', 'OPTIONS'])
def get_profile(profile_id):
    if request.method == 'OPTIONS':
        return '', 200
    
    profile = database.get_profile_by_id(profile_id)
    if not profile:
        return jsonify({"status": "error", "message": "Profile not found"}), 404
    
    return jsonify({"status": "success", "data": profile}), 200

# LIST all profiles (GET /api/profiles)
@app.route('/api/profiles', methods=['GET', 'OPTIONS'])
def list_profiles():
    if request.method == 'OPTIONS':
        return '', 200
    
    # Get filter parameters from the URL
    filters = {}
    if request.args.get('gender'):
        filters['gender'] = request.args.get('gender').lower()
    if request.args.get('country_id'):
        filters['country_id'] = request.args.get('country_id').upper()
    if request.args.get('age_group'):
        filters['age_group'] = request.args.get('age_group').lower()
    
    profiles = database.get_all_profiles(filters)
    
    return jsonify({
        "status": "success",
        "count": len(profiles),
        "data": profiles
    }), 200

# DELETE a profile (DELETE /api/profiles/{id})
@app.route('/api/profiles/<profile_id>', methods=['DELETE', 'OPTIONS'])
def delete_profile(profile_id):
    if request.method == 'OPTIONS':
        return '', 200
    
    deleted = database.delete_profile(profile_id)
    if not deleted:
        return jsonify({"status": "error", "message": "Profile not found"}), 404
    
    return '', 204

# Run the server (for local testing)
if __name__ == '__main__':
    print("🚀 Starting Profile Intelligence API...")
    print("📍 Local URL: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)