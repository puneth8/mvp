import sqlite3

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        skills TEXT,
        location TEXT,
        interest TEXT,
        experience INTEGER
    )
    """)

    # ---------------- RECOMMENDATIONS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_title TEXT,
        company TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ---------------- ADMIN TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ---------------- DEFAULT ADMIN ----------------
    cur.execute("""
    INSERT OR IGNORE INTO admin (username, password)
    VALUES ('admin', 'admin123')
    """)

    conn.commit()
    conn.close()
