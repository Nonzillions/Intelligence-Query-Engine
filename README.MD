# Intelligence Query Engine - HNG Internship Stage 2

## Live API
**Base URL:** `https://nonzillions.pythonanywhere.com`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profiles` | Query with filters, sorting, pagination |
| GET | `/api/profiles/search` | Natural language search |
| GET | `/api/profiles/{id}` | Get profile by ID |
| POST | `/api/profiles` | Create profile |
| DELETE | `/api/profiles/{id}` | Delete profile |

## Filtering Examples
/api/profiles?gender=male&country_id=NG
/api/profiles?min_age=25&max_age=40
/api/profiles?sort_by=age&order=desc
/api/profiles?page=2&limit=20

text

## Natural Language Search
/api/profiles/search?q=young males from nigeria
/api/profiles/search?q=females above 30
/api/profiles/search?q=adult males from kenya

text

## Response Format

```json
{
  "status": "success",
  "page": 1,
  "limit": 10,
  "total": 100,
  "data": [...]
}
Author
Nonzillions - HNG Internship

text

## 🚀 How to Deploy

1. **Save all files** to `~/HNG/profiles-api-stage2/`
2. **Upload to PythonAnywhere** (Files tab → `/home/Nonzillions/profiles-api-stage2/`)
3. **Go to Web tab** → Click **Reload**
4. **Run the grader again**

Let me know the result! 🎯
