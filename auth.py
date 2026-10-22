# auth.py
# This file handles user registration and login.

from database import get_connection
from models import Lecturer, CampusAdmin, SystemOperator
from security import hash_password, verify_password


def register_user(username, password, role, campus_id=None):
    # Adds a new user to the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, campus_id) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), role, campus_id)
        )
        conn.commit()
        return True, "Registration successful."
    except Exception as e:
        return False, f"Registration failed: {e}"
    finally:
        conn.close()


def login_user(username, password):
    # Checks username and password against the database
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Find the user by username ONLY
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # 2. Verify the password using our new security module
    if not verify_password(password, row["password"]):
        return None

    # 3. Return the correct object depending on the role
    role = row["role"]
    if role == "lecturer":
        return Lecturer(row["id"], row["username"], row["campus_id"])
    elif role == "admin":
        return CampusAdmin(row["id"], row["username"], row["campus_id"])
    elif role == "operator":
        return SystemOperator(row["id"], row["username"])
    return None