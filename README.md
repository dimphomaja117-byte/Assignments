# Smart Campus Resource Booking System

A desktop application built with Python and Tkinter for managing campus resource bookings across multiple campuses. The system supports three user roles — Lecturers, Campus Admins, and System Operators — each with their own dashboard and permissions.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [Installation & Setup](#installation--setup)
6. [Default Accounts](#default-accounts)
7. [Seeded Resources](#seeded-resources)
8. [User Roles & Permissions](#user-roles--permissions)
9. [Booking Rules Per Campus](#booking-rules-per-campus)
10. [Database Schema](#database-schema)
11. [How to Run](#how-to-run)
12. [Architecture & Design](#architecture--design)
13. [OOP Concepts Demonstrated](#oop-concepts-demonstrated)
14. [Security](#security)
15. [Known Limitations](#known-limitations)
16. [Possible Future Improvements](#possible-future-improvements)

---

## Overview

The Smart Campus Resource Booking System is a Python desktop application that allows lecturers to book campus resources (labs, projectors, etc.) while giving administrators and system operators the tools to manage resources and generate reports.

The system uses **SQLite** for data storage, **Tkinter** for the graphical interface, and follows a clean separation of concerns across multiple modules.

---

## Features

### Core Features
- **User Authentication** — Registration and login with securely salted password hashing (PBKDF2).
- **Role-Based Access Control** — Three distinct user roles with separate dashboards.
- **Multi-Campus Support** — Each campus has its own resources and booking rules.
- **Resource Booking** — Lecturers can book resources with date, time, and duration.
- **Booking Validation** — Enforces campus-specific duration limits and allowed hours.
- **Reports** — Campus summaries and cross-campus comparisons.

### Campus-Specific Booking Rules

| Campus | Max Duration | Allowed Hours | Priority Note |
|---|---|---|---|
| Centurion | 3 hours | 08:00 – 18:00 | Exam bookings first |
| Pretoria | 4 hours | 07:00 – 21:00 | Lecturers before 10:00 |
| Cape Town | 5 hours | 06:00 – 22:00 | First-come, first-served |

---

## Project Structure

```text
smart-campus-booking/
│
├── main.py                  # Application entry point
├── auth.py                  # Registration and login logic
├── database.py              # Database connection, schema, and seed data
├── models.py                # OOP classes (User, Lecturer, Admin, etc.)
├── booking_rules.py         # Campus-specific booking rule classes
├── reports.py               # Report generation functions
├── security.py              # Secure password hashing (PBKDF2)
│
└── gui/                     # GUI modules referenced by main.py
    ├── login_window.py
    ├── lecturer_window.py
    ├── admin_window.py
    └── operator_window.py
```

### Module Responsibilities

| File | Purpose |
|------|---------|
| `main.py` | Entry point; creates the root Tk window and handles login/logout routing |
| `auth.py` | User registration and secure login verification |
| `security.py` | Password hashing and verification using PBKDF2 with salts |
| `database.py` | SQLite connection management, table creation, and seeding data |
| `models.py` | Domain classes: `User` (abstract), `Lecturer`, `CampusAdmin`, `SystemOperator`, `Resource`, `Booking` |
| `booking_rules.py` | Base `BookingRule` class with subclass overrides per campus |
| `reports.py` | Functions for generating campus summary and comparison reports |
| `gui/` | Tkinter windows for each role's dashboard |

---

## Requirements

- **Python 3.8+**
- **Tkinter** (bundled with standard Python on most systems; on Linux you may need `sudo apt install python3-tk`)
- **SQLite3** (built into Python's standard library — no installation required)
- No third-party packages required.

---

## Installation & Setup

1. **Clone or extract the project** into a folder of your choice.
2. **Initialize the database** (creates tables, seeds default data and resources):
   ```bash
   python database.py
   ```
   You should see:
   ```text
   Database created successfully.
   Default data added.
   Resources added.
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

The `campus_booking.db` SQLite file will be created automatically in the project folder.

---

## Default Accounts

The database is seeded with the following accounts (using secure PBKDF2 hashing):

| Username | Password | Role | Campus |
|----------|----------|------|--------|
| `operator` | `Op3r@tor!2025` | System Operator | All campuses |
| `admin_cen` | `C3ntur!on#Adm` | Campus Admin | Centurion Campus |

> **Note:** If you need to reset the database to these defaults, simply delete `campus_booking.db` and run `python database.py` again.

---

## Seeded Resources

The database is pre-populated with 17 resources across the 3 campuses:

**Centurion Campus (5):** Lab A1, Lab A2, Lecture Hall C1, Projector P1, Meeting Room M1.
**Pretoria Campus (6):** Lab P1, Lab P2, Lecture Hall PR1, Projector PR2, Conference Room CR1, Study Room S1.
**Cape Town Campus (6):** Lab CT1, Lab CT2, Lecture Hall CT1, Projector CT-P1, Meeting Room CTM1, Study Room CTS1.

---

## User Roles & Permissions

### 🎓 Lecturer
- View available resources at their campus.
- Make bookings (subject to campus booking rules).
- View and cancel their own bookings.

### 🏫 Campus Admin
- Manage resources for their specific campus.
- View all bookings at their campus.
- Generate campus summary reports.

### ⚙️ System Operator
- Full system-wide access across all campuses.
- Compare statistics between campuses.
- Manage admins and users.
- Generate system-wide reports.

---

## Database Schema

### `campuses`
| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Unique campus name |
| `location` | TEXT | Human-readable location |

### `users`
| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key |
| `username` | TEXT | Unique |
| `password` | TEXT | Salted PBKDF2 hash |
| `role` | TEXT | `lecturer`, `admin`, or `operator` |
| `campus_id` | INTEGER | Foreign key → `campuses.id` |

### `resources`
| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Resource name |
| `type` | TEXT | e.g. "Computer Lab", "Projector" |
| `campus_id` | INTEGER | Foreign key → `campuses.id` |
| `capacity` | INTEGER | Seating capacity |

### `bookings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key |
| `user_id` | INTEGER | Foreign key → `users.id` |
| `resource_id` | INTEGER | Foreign key → `resources.id` |
| `campus_id` | INTEGER | Foreign key → `campuses.id` |
| `booking_date` | TEXT | Format: YYYY-MM-DD |
| `start_time` | TEXT | Format: HH:MM |
| `duration` | INTEGER | Hours |
| `status` | TEXT | `active` by default |

---

## Architecture & Design

The project follows a **layered architecture**:

```text
┌─────────────────────────────────────┐
│  Presentation Layer (gui/, main.py) │
│  Tkinter windows and routing        │
├─────────────────────────────────────┤
│  Business Logic Layer               │
│  auth.py, booking_rules.py,         │
│  reports.py, models.py, security.py │
├─────────────────────────────────────┤
│  Data Access Layer (database.py)    │
│  SQLite queries and schema          │
└─────────────────────────────────────┘
```

- **Separation of Concerns:** UI, business logic, and data access are decoupled.
- **Extensibility:** New campuses and roles can be added by extending existing classes and dictionaries.

---

## OOP Concepts Demonstrated

| Concept | Where |
|---------|-------|
| **Encapsulation** | `models.py` — `User` attributes use `_` prefix with `@property` getters |
| **Inheritance** | `Lecturer`, `CampusAdmin`, `SystemOperator` extend `User`; Campus rule classes extend `BookingRule` |
| **Abstraction** | `User` is an `ABC` with abstract `get_dashboard_title()` |
| **Polymorphism** | Each user role and booking rule overrides methods; `get_rule_for_campus()` returns the correct subclass |

---

## Security

- Passwords are **never** stored in plain text.
- Uses `hashlib.pbkdf2_hmac` with SHA-256, a random 16-byte salt, and 200,000 iterations.
- Protects against rainbow table attacks and brute-force cracking. 

---

## Known Limitations

- **No Conflict Detection** — The system does not currently check for double-bookings of the same resource at the same time.
- **Time Handling** — Times are stored as strings (`HH:MM`), not as structured time types.
- **GUI Dependencies** — The core `gui/` package referenced by `main.py` must be fully implemented to interact with the backend logic.

---

## Possible Future Improvements

- [ ] Add double-booking conflict detection.
- [ ] Add email/notification system for booking confirmations.
- [ ] Export reports to PDF or CSV.
- [ ] Add a calendar view for lecturers.
- [ ] Implement audit logging for admin actions.
- [ ] Add unit tests (pytest) for `booking_rules.py` and `security.py`.