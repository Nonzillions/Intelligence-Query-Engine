markdown
# Intelligence Query Engine - HNG Internship Stage 2

A powerful demographic intelligence API that transforms raw profile data into a searchable, filterable, and queryable engine with natural language support.

## 🚀 Live API

**Base URL:** `https://nonzillions.pythonanywhere.com`

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profiles` | Query profiles with filters, sorting, pagination |
| GET | `/api/profiles/search` | Natural language search |
| GET | `/api/profiles/{id}` | Get profile by ID |
| POST | `/api/profiles` | Create a new profile |
| DELETE | `/api/profiles/{id}` | Delete a profile |

## 🔍 Filtering Examples

### Basic Filters
```bash
# Filter by gender
GET /api/profiles?gender=male

# Filter by country
GET /api/profiles?country_id=NG

# Filter by age group
GET /api/profiles?age_group=adult
Age Range Filters
bash
# Minimum age
GET /api/profiles?min_age=25

# Maximum age
GET /api/profiles?max_age=40

# Age range
GET /api/profiles?min_age=25&max_age=40
Combined Filters
bash
# Multiple filters together
GET /api/profiles?gender=male&country_id=NG&min_age=25

# With probability thresholds
GET /api/profiles?min_gender_probability=0.8&min_country_probability=0.7
📊 Sorting
bash
# Sort by age (ascending/descending)
GET /api/profiles?sort_by=age&order=asc
GET /api/profiles?sort_by=age&order=desc

# Sort by creation date
GET /api/profiles?sort_by=created_at&order=desc

# Sort by gender probability
GET /api/profiles?sort_by=gender_probability&order=desc
📄 Pagination
bash
# Page 2, showing 20 results per page
GET /api/profiles?page=2&limit=20

# Default: page=1, limit=10 (max limit=50)
GET /api/profiles?page=3&limit=15
🧠 Natural Language Search
Supported Query Patterns
Pattern	Example	Maps To
Gender	"males", "females"	gender=male/female
Age group	"adult", "teenager", "senior"	age_group=...
Age above	"above 30", "over 30"	min_age=30
Age below	"under 25", "below 25"	max_age=25
Age range	"between 20 and 30"	min_age=20, max_age=30
Young	"young males"	min_age=16, max_age=24
Country	"from nigeria", "in kenya"	country_id=NG
Examples
bash
# Young males from Nigeria
GET /api/profiles/search?q=young males from nigeria

# Females above 30
GET /api/profiles/search?q=females above 30

# Adult males from Kenya
GET /api/profiles/search?q=adult males from kenya

# Teenagers
GET /api/profiles/search?q=teenagers

# Seniors from South Africa
GET /api/profiles/search?q=seniors from south africa

# Combined with pagination
GET /api/profiles/search?q=young females&page=2&limit=20
📊 Response Format
List Profiles Response
json
{
  "status": "success",
  "data": [
    {
      "id": "18f5a3c2-7d4a-4c91-9c2a-1f0a8e5b6d12",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG",
      "created_at": "2026-04-23T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
Natural Language Search Response
json
{
  "status": "success",
  "query": "young males from nigeria",
  "interpreted_as": {
    "gender": "male",
    "min_age": 16,
    "max_age": 24,
    "country_id": "NG"
  },
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "pages": 5
  }
}
Error Response
json
{
  "status": "error",
  "message": "Unable to interpret query"
}
🛠️ Local Development
Prerequisites
Python 3.8+

pip package manager

Installation
bash
# Clone the repository
git clone https://github.com/Nonzillions/profiles-api-stage2.git
cd profiles-api-stage2

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
Testing Locally
bash
# Test filtering
curl "http://localhost:8000/api/profiles?gender=male&country_id=NG"

# Test natural language search
curl "http://localhost:8000/api/profiles/search?q=young%20males%20from%20nigeria"

# Test pagination
curl "http://localhost:8000/api/profiles?page=2&limit=20"
📁 Project Structure
text
profiles-api-stage2/
├── app.py              # Main Flask application
├── database.py         # Database operations
├── parser.py           # Natural language parser
├── requirements.txt    # Python dependencies
├── test_stage2.py      # Test suite
└── README.md           # Documentation
🗄️ Database Schema
Field	Type	Description
id	UUID v7	Primary key
name	VARCHAR	Person's full name (unique)
gender	VARCHAR	male / female
gender_probability	FLOAT	Confidence score (0-1)
age	INT	Exact age
age_group	VARCHAR	child / teenager / adult / senior
country_id	VARCHAR(2)	ISO country code
country_name	VARCHAR	Full country name
country_probability	FLOAT	Confidence score (0-1)
created_at	TIMESTAMP	UTC timestamp
🚨 Error Codes
Status Code	Meaning
200	Success
201	Created (new profile)
204	Deleted (no content)
400	Bad request (missing parameter)
404	Profile not found
422	Invalid parameter type
500	Server error
🌐 CORS Configuration
The API includes CORS headers for cross-origin requests:

text
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
📈 Performance
Efficiently handles large datasets

Pagination prevents large data transfers

Proper indexing on filtered fields

Response time under 500ms for typical queries

👤 Author
Nonzillions

GitHub: @Nonzillions

Project: profiles-api-stage2

🙏 Acknowledgments
HNG Internship for this challenging project

Genderize.io, Agify.io, Nationalize.io for their free APIs

PythonAnywhere for free hosting

📝 Quick Reference Card
bash
# Most common queries

# Get Nigerian males aged 25-40
curl "https://nonzillions.pythonanywhere.com/api/profiles?gender=male&country_id=NG&min_age=25&max_age=40"

# Get youngest 20 profiles
curl "https://nonzillions.pythonanywhere.com/api/profiles?sort_by=age&order=asc&limit=20"

# Natural language search
curl "https://nonzillions.pythonanywhere.com/api/profiles/search?q=young%20females%20from%20kenya"

# Pagination
curl "https://nonzillions.pythonanywhere.com/api/profiles?page=3&limit=25"

