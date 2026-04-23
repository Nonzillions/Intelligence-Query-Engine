import sqlite3
import uuid
from datetime import datetime, timezone

def generate_uuid_v7():
    import time
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    return f"{timestamp:016x}-{random_part}"

# Sample profile data (you need at least 10-20 profiles for testing)
sample_profiles = [
    {"name": "john", "gender": "male", "gender_probability": 0.95, "age": 25, "age_group": "adult", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.85},
    {"name": "emmanuel", "gender": "male", "gender_probability": 0.92, "age": 30, "age_group": "adult", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.88},
    {"name": "sarah", "gender": "female", "gender_probability": 0.98, "age": 22, "age_group": "adult", "country_id": "KE", "country_name": "Kenya", "country_probability": 0.75},
    {"name": "mary", "gender": "female", "gender_probability": 0.97, "age": 18, "age_group": "teenager", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.82},
    {"name": "james", "gender": "male", "gender_probability": 0.94, "age": 45, "age_group": "adult", "country_id": "US", "country_name": "United States", "country_probability": 0.80},
    {"name": "lisa", "gender": "female", "gender_probability": 0.96, "age": 17, "age_group": "teenager", "country_id": "GB", "country_name": "United Kingdom", "country_probability": 0.78},
    {"name": "david", "gender": "male", "gender_probability": 0.93, "age": 35, "age_group": "adult", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.87},
    {"name": "grace", "gender": "female", "gender_probability": 0.99, "age": 28, "age_group": "adult", "country_id": "KE", "country_name": "Kenya", "country_probability": 0.76},
    {"name": "peter", "gender": "male", "gender_probability": 0.91, "age": 19, "age_group": "teenager", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.84},
    {"name": "ruth", "gender": "female", "gender_probability": 0.95, "age": 65, "age_group": "senior", "country_id": "US", "country_name": "United States", "country_probability": 0.81},
    {"name": "daniel", "gender": "male", "gender_probability": 0.90, "age": 12, "age_group": "child", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.83},
    {"name": "esther", "gender": "female", "gender_probability": 0.94, "age": 15, "age_group": "teenager", "country_id": "KE", "country_name": "Kenya", "country_probability": 0.77},
    {"name": "samuel", "gender": "male", "gender_probability": 0.89, "age": 8, "age_group": "child", "country_id": "GH", "country_name": "Ghana", "country_probability": 0.79},
    {"name": "deborah", "gender": "female", "gender_probability": 0.96, "age": 55, "age_group": "adult", "country_id": "NG", "country_name": "Nigeria", "country_probability": 0.86},
    {"name": "michael", "gender": "male", "gender_probability": 0.93, "age": 70, "age_group": "senior", "country_id": "US", "country_name": "United States", "country_probability": 0.82},
]

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

# Create table with CORRECT schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE,
        gender TEXT,
        gender_probability REAL,
        age INTEGER,
        age_group TEXT,
        country_id TEXT,
        country_name TEXT,
        country_probability REAL,
        created_at TEXT
    )
''')

# Insert sample data
count = 0
for profile in sample_profiles:
    cursor.execute("SELECT id FROM profiles WHERE name = ?", (profile['name'],))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO profiles (
                id, name, gender, gender_probability, age, age_group,
                country_id, country_name, country_probability, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            generate_uuid_v7(),
            profile['name'],
            profile['gender'],
            profile['gender_probability'],
            profile['age'],
            profile['age_group'],
            profile['country_id'],
            profile['country_name'],
            profile['country_probability'],
            datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        ))
        count += 1

conn.commit()
conn.close()

print(f"✅ Seeded {count} profiles into database")

# Verify
conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM profiles")
total = cursor.fetchone()[0]
print(f"📊 Total profiles in database: {total}")
conn.close()
