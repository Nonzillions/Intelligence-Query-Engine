import requests
import json

# Change this to your URL when deployed
BASE_URL = "http://localhost:8000"

def test_create_profile(name):
    print(f"\n📝 Creating profile for: {name}")
    response = requests.post(
        f"{BASE_URL}/api/profiles",
        json={"name": name}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response

def test_list_profiles():
    print(f"\n📋 Listing all profiles")
    response = requests.get(f"{BASE_URL}/api/profiles")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response

def test_get_profile(profile_id):
    print(f"\n🔍 Getting profile: {profile_id}")
    response = requests.get(f"{BASE_URL}/api/profiles/{profile_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response

def test_delete_profile(profile_id):
    print(f"\n🗑️ Deleting profile: {profile_id}")
    response = requests.delete(f"{BASE_URL}/api/profiles/{profile_id}")
    print(f"Status: {response.status_code}")
    return response

if __name__ == "__main__":
    print("="*50)
    print("🧪 Testing Profile API")
    print("="*50)
    
    # Test 1: Create a profile
    result = test_create_profile("ella")
    
    # Get the ID from the response
    profile_id = None
    if result.status_code in [200, 201]:
        profile_id = result.json().get('data', {}).get('id')
        print(f"\n✅ Got ID: {profile_id}")
    
    # Test 2: Same name again (idempotency)
    test_create_profile("ella")
    
    # Test 3: Create another profile
    test_create_profile("john")
    
    # Test 4: List all profiles
    test_list_profiles()
    
    # Test 5: Get profile by ID
    if profile_id:
        test_get_profile(profile_id)
    
    # Test 6: Delete profile
    if profile_id:
        test_delete_profile(profile_id)
        
        # Verify it's gone
        test_get_profile(profile_id)
    
    print("\n" + "="*50)
    print("✅ Testing Complete!")