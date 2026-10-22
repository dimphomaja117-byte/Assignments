# booking_rules.py
# This file contains booking rules for each campus.
# Each campus has its own max duration, allowed hours, and priority note.


# -------- Base Booking Rule --------
class BookingRule:
    # Default rules used if a campus has no custom rule

    def __init__(self, campus_name):
        self.campus_name = campus_name

    def max_duration(self):
        # Maximum hours allowed per booking
        return 4

    def allowed_hours(self):
        # Returns (opening_hour, closing_hour) in 24-hour format
        return (7, 21)

    def priority_note(self):
        # Any special priority access note
        return "No priority access rules."

    def validate(self, booking_date, start_time, duration):
        # Returns (True, message) if the booking is valid, else (False, error)
        # Check duration limit
        if duration > self.max_duration():
            return False, f"Max duration at {self.campus_name} is {self.max_duration()} hours."

        if duration <= 0:
            return False, "Duration must be at least 1 hour."

        # Check starting hour
        try:
            start_hour = int(start_time.split(":")[0])
        except (ValueError, IndexError):
            return False, "Invalid time format. Use HH:MM."

        open_hour, close_hour = self.allowed_hours()
        if start_hour < open_hour or start_hour >= close_hour:
            return False, (f"Bookings at {self.campus_name} are only allowed "
                           f"between {open_hour:02d}:00 and {close_hour:02d}:00.")

        # Make sure booking doesn't run past closing time
        if start_hour + duration > close_hour:
            return False, f"Booking would end after {close_hour:02d}:00."

        return True, "Booking is valid."


# -------- Centurion Rules --------
class CenturionRule(BookingRule):
    # Centurion: max 3 hours, 08:00 to 18:00

    def __init__(self):
        super().__init__("Centurion Campus")

    def max_duration(self):
        return 3

    def allowed_hours(self):
        return (8, 18)

    def priority_note(self):
        return "Priority: Exam bookings first."


# -------- Pretoria Rules --------
class PretoriaRule(BookingRule):
    # Pretoria: max 4 hours, 07:00 to 21:00

    def __init__(self):
        super().__init__("Pretoria Campus")

    def max_duration(self):
        return 4

    def allowed_hours(self):
        return (7, 21)

    def priority_note(self):
        return "Priority: Lecturers before 10:00."


# -------- Cape Town Rules --------
class CapeTownRule(BookingRule):
    # Cape Town: max 5 hours, 06:00 to 22:00

    def __init__(self):
        super().__init__("Cape Town Campus")

    def max_duration(self):
        return 5

    def allowed_hours(self):
        return (6, 22)

    def priority_note(self):
        return "Priority: First-come, first-served."


# -------- Registry --------
# Maps campus name to its rule class. Adding a new campus is easy:
# just create a new class above and add it here.

CAMPUS_RULES = {
    "Centurion Campus": CenturionRule,
    "Pretoria Campus": PretoriaRule,
    "Cape Town Campus": CapeTownRule,
}


def get_rule_for_campus(campus_name):
    # Returns the correct BookingRule object for a given campus
    rule_class = CAMPUS_RULES.get(campus_name, BookingRule)
    return rule_class()