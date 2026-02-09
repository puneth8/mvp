from database import get_connection

# ---------------- USER REGISTRATION ----------------
def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

# ---------------- USER LOGIN ----------------
def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cur.fetchone()
    conn.close()
    return user

# ---------------- UPDATE USER PROFILE ----------------
def update_user_profile(user_id, skills, location, interest, experience):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET skills = ?, location = ?, interest = ?, experience = ?
        WHERE id = ?
        """,
        (skills, location, interest, experience, user_id)
    )

    conn.commit()
    conn.close()

# ---------------- GET USER BY ID ----------------
def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cur.fetchone()
    conn.close()
    return user
