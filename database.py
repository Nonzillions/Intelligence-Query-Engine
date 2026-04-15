import sqlite3
import uuid
from datetime import datetime, timezone

# Connect to the database (creates a file called profiles.db)
def get_db():
    conn = sqlite3.connect('profiles.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table (like a spreadsheet) if it doesn't exist
def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            gender TEXT,
            gender_probability REAL,
            sample_size INTEGER,
            age INTEGER,
            age_group TEXT,
            country_id TEXT,
            country_probability REAL,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database ready!")

# Create a unique ID (UUID v7 style)
def generate_uuid_v7():
    import time
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    return f"{timestamp:016x}-{random_part}"

# Save a profile, or return existing one if name already exists
def save_profile(profile_data):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if this name already exists
    cursor.execute("SELECT * FROM profiles WHERE name = ?", (profile_data['name'],))
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return dict(existing), True  # True means "already exists"
    
    # Insert new profile
    cursor.execute('''
        INSERT INTO profiles (
            id, name, gender, gender_probability, sample_size,
            age, age_group, country_id, country_probability, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        profile_data['id'], profile_data['name'], profile_data['gender'],
        profile_data['gender_probability'], profile_data['sample_size'],
        profile_data['age'], profile_data['age_group'], profile_data['country_id'],
        profile_data['country_probability'], profile_data['created_at']
    ))
    
    conn.commit()
    conn.close()
    return profile_data, False  # False means "newly created"

# Get a profile by its ID
def get_profile_by_id(profile_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None

# Get all profiles, optionally filtered
def get_all_profiles(filters=None):
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT id, name, gender, age, age_group, country_id FROM profiles WHERE 1=1"
    params = []
    
    if filters:
        if filters.get('gender'):
            query += " AND gender = ?"
            params.append(filters['gender'])
        if filters.get('country_id'):
            query += " AND country_id = ?"
            params.append(filters['country_id'])
        if filters.get('age_group'):
            query += " AND age_group = ?"
            params.append(filters['age_group'])
    
    cursor.execute(query, params)
    profiles = cursor.fetchall()
    conn.close()
    return [dict(profile) for profile in profiles]

# Delete a profile by ID
def delete_profile(profile_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted