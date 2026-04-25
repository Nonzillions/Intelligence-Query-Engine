# Intelligence Query Engine - HNG Internship Stage 2

A powerful demographic intelligence API that transforms raw profile data into a searchable, filterable, and queryable engine. This system allows marketing teams, product managers, and growth analysts to segment users, identify patterns, and query large datasets using natural language.

## 🚀 Live Demo

**Base URL:** `https://nonzillions.pythonanywhere.com`

## 📚 Overview

This API builds on the Profile Intelligence Service from Stage 1, adding:
- Advanced filtering with multiple conditions
- Sorting and pagination
- Natural language query parsing
- Combined filter support
- Efficient database querying

## 🎯 Features

### 1. Advanced Filtering
Filter profiles by multiple criteria simultaneously:
- `gender` - male/female
- `age_group` - child/teenager/adult/senior
- `country_id` - ISO country code (NG, US, KE, etc.)
- `min_age` / `max_age` - Age range filtering
- `min_gender_probability` - Minimum confidence score
- `min_country_probability` - Minimum country confidence

### 2. Sorting
Sort results by any field:
- `sort_by` - age | created_at | gender_probability
- `order` - asc | desc

### 3. Pagination
Navigate through large datasets efficiently:
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10, max: 50)

### 4. Natural Language Search
Search using plain English queries:
- "young males from nigeria"
- "females above 30"
- "people from angola"
- "adult males from kenya"

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profiles` | Query profiles with filters, sorting, pagination |
| GET | `/api/profiles/search` | Natural language search |
| GET | `/api/profiles/{id}` | Get profile by ID |
| POST | `/api/profiles` | Create a new profile |
| DELETE | `/api/profiles/{id}` | Delete a profile |

## 🔍 Query Examples

### Basic Filtering
```bash
# Get all male profiles from Nigeria
GET /api/profiles?gender=male&country_id=NG

# Get adults aged 25-40
GET /api/profiles?age_group=adult&min_age=25&max_age=40

# High confidence predictions
GET /api/profiles?min_gender_probability=0.9&min_country_probability=0.8
Sorting
bash
# Youngest first
GET /api/profiles?sort_by=age&order=asc

# Oldest first
GET /api/profiles?sort_by=age&order=desc

# Most confident predictions first
GET /api/profiles?sort_by=gender_probability&order=desc
Pagination
bash
# Page 2, show 20 results per page
GET /api/profiles?page=2&limit=20
Combined Filters
bash
# Adult males from Nigeria, aged 30-50, sorted by age
GET /api/profiles?gender=male&age_group=adult&country_id=NG&min_age=30&max_age=50&sort_by=age&order=asc
Natural Language Search
bash
# Search for young males from Nigeria
GET /api/profiles/search?q=young males from nigeria

# Search for females over 30
GET /api/profiles/search?q=females above 30

# Search with pagination
GET /api/profiles/search?q=adult males from kenya&page=2&limit=20
📊 Response Format
List Profiles Response
json
{
  "status": "success",
  "page": 1,
  "limit": 10,
  "total": 2026,
  "data": [
    {
      "id": "18f5a3c2-7d4a-4c91-9c2a-1f0a8e5b6d12",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG",
      "created_at": "2026-04-21T12:00:00Z"
    }
  ]
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
  "page": 1,
  "limit": 10,
  "total": 45,
  "data": [...]
}
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
🧪 Natural Language Parsing Rules
Natural Language	Interpreted As
"young"	min_age=16, max_age=24
"male / men / boys"	gender=male
"female / women / girls"	gender=female
"child / children / kids"	age_group=child
"teenager / teens"	age_group=teenager
"adult / adults"	age_group=adult
"senior / elderly / old"	age_group=senior
"above X / over X / older than X"	min_age=X
"below X / under X / younger than X"	max_age=X
"from [country]"	country_id=[code]
🛠️ Local Development
Prerequisites
Python 3.8+

pip package manager

Installation
bash
# Clone the repository
git clone https://github.com/Nonzillions/Data-Persistence-API-Design.git
cd Data-Persistence-API-Design

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
Testing
bash
# Run the test suite
python test_stage2.py

# Manual testing with curl
curl "http://localhost:8000/api/profiles?gender=male&country_id=NG&min_age=25"
curl "http://localhost:8000/api/profiles/search?q=young%20males%20from%20nigeria"
🚀 Deployment
This API is deployed on PythonAnywhere (free tier).

Deployment Steps:
Upload files to /home/Nonzillions/profiles-api/

Install dependencies: pip3.8 install --user -r requirements.txt

Configure WSGI file to point to app.py

Reload the web application

📁 Project Structure
text
profiles-api/
├── app.py              # Main Flask application
├── database.py         # Database operations
├── parser.py           # Natural language parser
├── requirements.txt    # Python dependencies
├── test_stage2.py      # Test suite
└── README.md           # This file
🚨 Error Handling
All errors follow this structure:

json
{
  "status": "error",
  "message": "Error description here"
}
Status Code	Meaning
200	Success
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
Efficiently handles 2026+ profiles

Pagination prevents large data transfers

Proper indexing on filtered fields

Response time under 500ms for typical queries

🔮 Future Improvements
Add more natural language patterns

Implement caching for frequent queries

Add export functionality (CSV/JSON)

Create analytics endpoints

Add API rate limiting

Implement full-text search on names

👤 Author
Nonzillions

GitHub: @Nonzillions

Project: Data-Persistence-API-Design

🙏 Acknowledgments
HNG Internship for this challenging project

Genderize.io, Agify.io, and Nationalize.io for their free APIs

PythonAnywhere for free hosting

📝 Quick Reference Card
Most Common Queries
bash
# Get Nigerian males aged 25-40
curl "https://nonzillions.pythonanywhere.com/api/profiles?gender=male&country_id=NG&min_age=25&max_age=40"

# Get youngest 20 profiles
curl "https://nonzillions.pythonanywhere.com/api/profiles?sort_by=age&order=asc&limit=20"

# Search natural language
curl "https://nonzillions.pythonanywhere.com/api/profiles/search?q=young%20females%20from%20kenya"

