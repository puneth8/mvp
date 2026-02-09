from database import get_connection

def admin_login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM admin
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    admin = cur.fetchone()
    conn.close()
    return admin
