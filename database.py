import sqlite3
import datetime
import json
from config import DATABASE_URL, LOG_FILE

def get_db_connection():
    """Establish a connection to the SQLite database."""
    # Remove 'sqlite:///' from the URL if it's there
    db_path = DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        skill_level TEXT DEFAULT 'beginner',
        session_count INTEGER DEFAULT 0,
        last_active TIMESTAMP,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Topics and Knowledge Graph
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_knowledge (
        user_id INTEGER,
        topic TEXT,
        mastery_score REAL DEFAULT 0.0,
        status TEXT DEFAULT 'new', -- 'new', 'learning', 'mastered', 'weak'
        last_reviewed TIMESTAMP,
        review_interval INTEGER DEFAULT 1, -- in days for SM-2
        easiness_factor REAL DEFAULT 2.5, -- for SM-2
        repetitions INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, topic)
    )
    ''')

    # Learning History (Extension 1)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interaction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT, -- 'user' or 'bot'
        content TEXT,
        topic TEXT,
        difficulty_level TEXT,
        concept_tagged TEXT,
        error_type TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Quiz results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        score REAL,
        total_questions INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Spaced Repetition Tasks (Extension 3)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        concept TEXT,
        due_date DATE,
        completed BOOLEAN DEFAULT FALSE
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# --- CRUD Operations ---

def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def create_or_update_user(user_id, username, first_name):
    conn = get_db_connection()
    now = datetime.datetime.now()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    if user:
        conn.execute('''
            UPDATE users SET username = ?, first_name = ?, last_active = ?, session_count = session_count + 1 
            WHERE user_id = ?
        ''', (username, first_name, now, user_id))
    else:
        conn.execute('''
            INSERT INTO users (user_id, username, first_name, last_active, session_count) 
            VALUES (?, ?, ?, ?, 1)
        ''', (user_id, username, first_name, now))
    
    conn.commit()
    conn.close()

def log_interaction(user_id, role, content, topic=None, difficulty=None, concept=None, error=None):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO interaction_logs (user_id, role, content, topic, difficulty_level, concept_tagged, error_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, role, content, topic, difficulty, concept, error))
    conn.commit()
    conn.close()

def get_last_interactions(user_id, limit=10):
    conn = get_db_connection()
    logs = conn.execute('''
        SELECT role, content FROM interaction_logs 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT ?
    ''', (user_id, limit)).fetchall()
    conn.close()
    return logs[::-1] # Return in chronological order

def update_knowledge(user_id, topic, score_delta=None, status=None, mastery=None):
    conn = get_db_connection()
    existing = conn.execute('SELECT * FROM user_knowledge WHERE user_id = ? AND topic = ?', 
                           (user_id, topic)).fetchone()
    
    now = datetime.datetime.now()
    if existing:
        updates = []
        params = []
        if mastery is not None:
            updates.append("mastery_score = ?")
            params.append(mastery)
        elif score_delta is not None:
            updates.append("mastery_score = mastery_score + ?")
            params.append(score_delta)
        
        if status:
            updates.append("status = ?")
            params.append(status)
        
        updates.append("last_reviewed = ?")
        params.append(now)
        
        params.append(user_id)
        params.append(topic)
        
        query = f"UPDATE user_knowledge SET {', '.join(updates)} WHERE user_id = ? AND topic = ?"
        conn.execute(query, tuple(params))
    else:
        mastery = mastery if mastery is not None else (score_delta if score_delta else 0.0)
        status = status if status else 'learning'
        conn.execute('''
            INSERT INTO user_knowledge (user_id, topic, mastery_score, status, last_reviewed)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, topic, mastery, status, now))
    
    conn.commit()
    conn.close()

def get_user_weak_areas(user_id, threshold=0.7):
    conn = get_db_connection()
    weak = conn.execute('''
        SELECT topic FROM user_knowledge 
        WHERE user_id = ? AND (mastery_score < ? OR status = 'weak')
    ''', (user_id, threshold)).fetchall()
    conn.close()
    return [row['topic'] for row in weak]

def get_due_reviews(user_id):
    today = datetime.date.today()
    conn = get_db_connection()
    due = conn.execute('''
        SELECT topic, concept FROM review_schedule 
        WHERE user_id = ? AND due_date <= ? AND completed = FALSE
    ''', (user_id, today)).fetchall()
    conn.close()
    return due

def save_quiz_result(user_id, topic, score, total):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO quiz_results (user_id, topic, score, total_questions)
        VALUES (?, ?, ?, ?)
    ''', (user_id, topic, score, total))
    
    # Update knowledge based on quiz
    percentage = score / total if total > 0 else 0
    status = 'mastered' if percentage >= 0.9 else ('weak' if percentage < 0.7 else 'learning')
    
    update_knowledge(user_id, topic, mastery=percentage, status=status)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
