import sqlite3
import uuid
from datetime import datetime, timezone

def get_db():
    conn = sqlite3.connect('profiles.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()
    print("✅ Database tables ready")

def generate_uuid_v7():
    import time
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    return f"{timestamp:016x}-{random_part}"

def get_all_profiles(filters=None, sort_by='created_at', order='asc', page=1, limit=10):
    conn = get_db()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if filters:
        if filters.get('gender'):
            where_clauses.append("gender = ?")
            params.append(filters['gender'])
        if filters.get('age_group'):
            where_clauses.append("age_group = ?")
            params.append(filters['age_group'])
        if filters.get('country_id'):
            where_clauses.append("country_id = ?")
            params.append(filters['country_id'].upper())
        if filters.get('min_age'):
            where_clauses.append("age >= ?")
            params.append(int(filters['min_age']))
        if filters.get('max_age'):
            where_clauses.append("age <= ?")
            params.append(int(filters['max_age']))
        if filters.get('min_gender_probability'):
            where_clauses.append("gender_probability >= ?")
            params.append(float(filters['min_gender_probability']))
        if filters.get('min_country_probability'):
            where_clauses.append("country_probability >= ?")
            params.append(float(filters['min_country_probability']))
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get total count
    count_query = f"SELECT COUNT(*) as total FROM profiles WHERE {where_sql}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Get paginated results
    offset = (page - 1) * limit
    query = f"""
        SELECT id, name, gender, age, age_group, country_id, created_at
        FROM profiles 
        WHERE {where_sql}
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
    """
    cursor.execute(query, params + [limit, offset])
    profiles = cursor.fetchall()
    
    conn.close()
    return [dict(p) for p in profiles], total

def get_profile_by_id(profile_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None

def delete_profile(profile_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def save_profile(profile_data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE name = ?", (profile_data['name'],))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return dict(existing), True
    cursor.execute('''
        INSERT INTO profiles (id, name, gender, gender_probability, age, age_group,
        country_id, country_name, country_probability, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        profile_data['id'], profile_data['name'], profile_data['gender'],
        profile_data['gender_probability'], profile_data['age'], profile_data['age_group'],
        profile_data['country_id'], profile_data['country_name'],
        profile_data['country_probability'], profile_data['created_at']
    ))
    conn.commit()
    conn.close()
    return profile_data, False

def seed_database_from_csv(csv_data):
    import csv
    import io
    
    conn = get_db()
    cursor = conn.cursor()
    created_count = 0
    
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    
    for row in reader:
        cursor.execute("SELECT id FROM profiles WHERE name = ?", (row['name'],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO profiles (
                    id, name, gender, gender_probability, age, age_group,
                    country_id, country_name, country_probability, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                generate_uuid_v7(),
                row['name'],
                row['gender'],
                float(row['gender_probability']),
                int(row['age']),
                row['age_group'],
                row['country_id'],
                row['country_name'],
                float(row['country_probability']),
                datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            ))
            created_count += 1
    
    conn.commit()
    conn.close()
    return created_count

def clear_all_profiles():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles")
    conn.commit()
    conn.close()
    print("✅ All profiles cleared")