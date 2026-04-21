import requests
import json

BASE_URL = "http://localhost:8000"

def test_filtering():
    print("\n" + "="*60)
    print("📋 TEST 1: Advanced Filtering")
    print("="*60)
    
    # Test 1a: Simple filter
    response = requests.get(f"{BASE_URL}/api/profiles?gender=male&country_id=NG&min_age=25")
    print(f"\n1a. Filter: gender=male, country_id=NG, min_age=25")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total: {data['total']}")
        print(f"First result: {data['data'][0] if data['data'] else 'None'}")

def test_sorting():
    print("\n" + "="*60)
    print("📋 TEST 2: Sorting")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/profiles?sort_by=age&order=desc&limit=5")
    print(f"\n2. Sort by age DESC (oldest first)")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        for profile in data['data']:
            print(f"   - {profile['name']}: age {profile['age']}")

def test_pagination():
    print("\n" + "="*60)
    print("📋 TEST 3: Pagination")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/profiles?page=2&limit=5")
    print(f"\n3. Page 2, Limit 5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Page: {data['page']}")
        print(f"Limit: {data['limit']}")
        print(f"Total: {data['total']}")
        print(f"Profiles on this page: {len(data['data'])}")

def test_natural_language():
    print("\n" + "="*60)
    print("📋 TEST 4: Natural Language Search")
    print("="*60)
    
    queries = [
        "young males from nigeria",
        "females above 30",
        "people from angola",
        "adult males from kenya",
        "teenagers",
        "invalid query xyz123"
    ]
    
    for query in queries:
        response = requests.get(f"{BASE_URL}/api/profiles/search?q={query}")
        print(f"\n4. Query: '{query}'")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Interpreted as: {data.get('interpreted_as', {})}")
            print(f"Total results: {data['total']}")
        else:
            print(f"Message: {response.json().get('message')}")

def test_combined_filters():
    print("\n" + "="*60)
    print("📋 TEST 5: Combined Filters")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/api/profiles",
        params={
            'gender': 'male',
            'age_group': 'adult',
            'country_id': 'NG',
            'min_age': 25,
            'max_age': 40,
            'min_gender_probability': 0.8,
            'sort_by': 'age',
            'order': 'asc',
            'page': 1,
            'limit': 10
        }
    )
    print(f"\n5. Combined filters (male, adult, Nigeria, age 25-40)")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total results: {data['total']}")

if __name__ == "__main__":
    print("🚀 Testing Stage 2: Intelligence Query Engine")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/", timeout=5)
    except:
        print("❌ Server not running! Start with: python app.py")
        exit(1)
    
    test_filtering()
    test_sorting()
    test_pagination()
    test_natural_language()
    test_combined_filters()
    
    print("\n" + "="*60)
    print("✅ Testing Complete!")