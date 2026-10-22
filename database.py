# database.py
# This file handles the SQLite database connection, table creation, and default data.

import sqlite3   # Built-in library for SQLite database
from security import hash_password  # Secure password hashing

# The database file will be created in the project folder
DB_NAME = "campus_booking.db"


def get_connection():
    # Opens a connection to the database
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # Allows access by column name
    return conn


def initialize_database():
    # Creates all required tables if they don't exist yet
    conn = get_connection()
    cursor = conn.cursor()

    # Campuses table - stores each campus
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            location TEXT
        )
    """)

    # Users table - stores all user accounts (lecturer / admin / operator)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            campus_id INTEGER,
            FOREIGN KEY (campus_id) REFERENCES campuses(id)
        )
    """)

    # Resources table - stores resources like labs, projectors, etc.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            campus_id INTEGER NOT NULL,
            capacity INTEGER,
            UNIQUE(name, campus_id),
            FOREIGN KEY (campus_id) REFERENCES campuses(id)
        )
    """)

    # Bookings table - stores all bookings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            campus_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (resource_id) REFERENCES resources(id),
            FOREIGN KEY (campus_id) REFERENCES campuses(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database created successfully.")


def seed_data():
    # Adds default campuses and default admin/operator accounts
    conn = get_connection()
    cursor = conn.cursor()

    # 3 default campuses
    campuses = [
        ("Centurion Campus", "Centurion, Gauteng"),
        ("Pretoria Campus", "Pretoria CBD, Gauteng"),
        ("Cape Town Campus", "Cape Town CBD"),
    ]
    for name, location in campuses:
        try:
            cursor.execute(
                "INSERT INTO campuses (name, location) VALUES (?, ?)",
                (name, location)
            )
        except sqlite3.IntegrityError:
            pass   # Campus already exists, skip it

    # Default system operator
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, campus_id) VALUES (?, ?, ?, ?)",
            ("operator", hash_password("Op3r@tor!2025"), "operator", None)
        )
    except sqlite3.IntegrityError:
        pass

    # Default admin for Centurion campus (campus_id = 1)
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, campus_id) VALUES (?, ?, ?, ?)",
            ("admin_cen", hash_password("C3ntur!on#Adm"), "admin", 1)
        )
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
    print("Default data added.")


def seed_resources():
    # Adds default resources for each campus (safe to re-run)
    conn = get_connection()
    cursor = conn.cursor()

    # Look up campus IDs by name so we don't hard-code 1/2/3
    cursor.execute("SELECT id, name FROM campuses")
    campus_map = {row["name"]: row["id"] for row in cursor.fetchall()}

    # resource tuple: (campus_name, name, type, capacity)
    resources = [
        # ---- Centurion Campus ----
        ("Centurion Campus", "Lab A1", "Computer Lab", 30),
        ("Centurion Campus", "Lab A2", "Computer Lab", 25),
        ("Centurion Campus", "Lecture Hall C1", "Lecture Hall", 120),
        ("Centurion Campus", "Projector P1", "Projector", 1),
        ("Centurion Campus", "Meeting Room M1", "Meeting Room", 10),

        # ---- Pretoria Campus ----
        ("Pretoria Campus", "Lab P1", "Computer Lab", 40),
        ("Pretoria Campus", "Lab P2", "Computer Lab", 35),
        ("Pretoria Campus", "Lecture Hall PR1", "Lecture Hall", 200),
        ("Pretoria Campus", "Projector PR2", "Projector", 1),
        ("Pretoria Campus", "Conference Room CR1", "Meeting Room", 15),
        ("Pretoria Campus", "Study Room S1", "Study Room", 6),

        # ---- Cape Town Campus ----
        ("Cape Town Campus", "Lab CT1", "Computer Lab", 28),
        ("Cape Town Campus", "Lab CT2", "Computer Lab", 32),
        ("Cape Town Campus", "Lecture Hall CT1", "Lecture Hall", 150),
        ("Cape Town Campus", "Projector CT-P1", "Projector", 1),
        ("Cape Town Campus", "Meeting Room CTM1", "Meeting Room", 12),
        ("Cape Town Campus", "Study Room CTS1", "Study Room", 8),
    ]

    for campus_name, name, type_, capacity in resources:
        campus_id = campus_map.get(campus_name)
        if campus_id is None:
            print(f"Skipping '{name}' — campus '{campus_name}' not found.")
            continue
        try:
            cursor.execute(
                "INSERT INTO resources (name, type, campus_id, capacity) "
                "VALUES (?, ?, ?, ?)",
                (name, type_, campus_id, capacity)
            )
        except sqlite3.IntegrityError:
            pass  # Already exists (UNIQUE on name + campus_id)

    conn.commit()
    conn.close()
    print("Resources added.")


# This runs only if you execute database.py directly
if __name__ == "__main__":
    initialize_database()
    seed_data()
    seed_resources()