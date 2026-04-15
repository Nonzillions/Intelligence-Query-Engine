cd ~/HNG/profiles-api

cat > README.md << 'EOF'
# Profile Intelligence Service - HNG Internship Stage 1

A comprehensive REST API that enriches name data using multiple external APIs, stores results in a database, and provides full CRUD operations with intelligent idempotency.

## 🚀 Live Demo

**Base URL:** `https://nonzillions.pythonanywhere.com`

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/profiles` | Create a new profile from a name |
| GET | `/api/profiles/{id}` | Retrieve a profile by UUID |
| GET | `/api/profiles` | List all profiles with optional filters |
| DELETE | `/api/profiles/{id}` | Delete a profile |

---

## 📖 API Documentation

### 1. POST /api/profiles - Create Profile

Creates a new profile by enriching the name with data from three external APIs.

**Request Body:**
```json
{
  "name": "ella"
}


{
  "status": "success",
  "data": {
    "id": "18f5a3c2-7d4a-4c91-9c2a-1f0a8e5b6d12",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "DRC",
    "country_probability": 0.85,
    "created_at": "2026-04-15T12:00:00Z"
  }
}

{
  "status": "success",
  "message": "Profile already exists",
  "data": { ...existing profile... }
}
Error Responses:

Status Code	Condition
400	Missing or empty name
422	Name is not a string
502	External API returned invalid data
500	Server error
2. GET /api/profiles/{id} - Retrieve Profile
Fetches a single profile by its UUID

Success Response (200 OK):

json
{
  "status": "success",
  "data": {
    "id": "18f5a3c2-7d4a-4c91-9c2a-1f0a8e5b6d12",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "DRC",
    "country_probability": 0.85,
    "created_at": "2026-04-15T12:00:00Z"
  }
}

Error Response (404 Not Found):

json
{
  "status": "error",
  "message": "Profile not found"
}
3. GET /api/profiles - List Profiles
Returns a list of all profiles with optional filtering.

Query Parameters (all optional, case-insensitive):

Parameter	Description	Example
gender	Filter by gender	male, female
country_id	Filter by country code	NG, US, DRC
age_group	Filter by age group	child, teenager, adult, senior
Example Requests:

bash
# List all profiles
GET /api/profiles

# Filter by gender
GET /api/profiles?gender=male

# Filter by country
GET /api/profiles?country_id=NG

# Multiple filters
GET /api/profiles?gender=female&country_id=DRC
Success Response (200 OK):

json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "18f5a3c2-7d4a-4c91-9c2a-1f0a8e5b6d12",
      "name": "ella",
      "gender": "female",
      "age": 46,
      "age_group": "adult",
      "country_id": "DRC"
    },
    {
      "id": "92b7d1e4-3f5a-4b8c-9d2e-6a1f3c8e5b7d",
      "name": "john",
      "gender": "male",
      "age": 45,
      "age_group": "adult",
      "country_id": "US"
    }
  ]
}
4. DELETE /api/profiles/{id} - Delete Profile
Permanently removes a profile from the database.

Success Response (204 No Content):

text
(empty response body)
Error Response (404 Not Found):

json
{
  "status": "error",
  "message": "Profile not found"
}
