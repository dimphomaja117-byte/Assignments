# models.py
# This file contains the OOP classes: User, Lecturer, CampusAdmin,
# SystemOperator, Resource, and Booking.

from abc import ABC, abstractmethod   # For abstract base classes


# -------- Base User class --------
class User(ABC):
    # Abstract base class for all user roles.
    # Uses encapsulation (protected attributes starting with _)

    def __init__(self, user_id, username, role, campus_id=None):
        self._user_id = user_id
        self._username = username
        self._role = role
        self._campus_id = campus_id

    # Getters using @property (encapsulation)
    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @property
    def role(self):
        return self._role

    @property
    def campus_id(self):
        return self._campus_id

    # Every subclass must implement this
    @abstractmethod
    def get_dashboard_title(self):
        pass


# -------- Lecturer (inherits from User) --------
class Lecturer(User):
    # A lecturer who books resources

    def __init__(self, user_id, username, campus_id=None):
        super().__init__(user_id, username, "lecturer", campus_id)

    def get_dashboard_title(self):
        return f"Lecturer Dashboard - {self.username}"


# -------- Campus Admin (inherits from User) --------
class CampusAdmin(User):
    # Manages resources for one campus

    def __init__(self, user_id, username, campus_id):
        super().__init__(user_id, username, "admin", campus_id)

    def get_dashboard_title(self):
        return f"Campus Admin Dashboard - {self.username}"


# -------- System Operator (inherits from User) --------
class SystemOperator(User):
    # Has system-wide access across all campuses

    def __init__(self, user_id, username):
        super().__init__(user_id, username, "operator", None)

    def get_dashboard_title(self):
        return f"System Operator Dashboard - {self.username}"


# -------- Resource --------
class Resource:
    # A bookable resource such as a lab or projector

    def __init__(self, resource_id, name, type_, campus_id, capacity=0):
        self.resource_id = resource_id
        self.name = name
        self.type = type_
        self.campus_id = campus_id
        self.capacity = capacity

    def __str__(self):
        return f"{self.name} ({self.type}) - Capacity {self.capacity}"


# -------- Booking --------
class Booking:
    # A single booking made by a user

    def __init__(self, booking_id, user_id, resource_id, campus_id,
                 booking_date, start_time, duration, status="active"):
        self.booking_id = booking_id
        self.user_id = user_id
        self.resource_id = resource_id
        self.campus_id = campus_id
        self.booking_date = booking_date
        self.start_time = start_time
        self.duration = duration
        self.status = status

    def __str__(self):
        return (f"Booking #{self.booking_id}: "
                f"Resource {self.resource_id} on {self.booking_date} "
                f"at {self.start_time} for {self.duration}h")