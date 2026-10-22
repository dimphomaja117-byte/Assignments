# main.py
# Entry point for the Smart Campus Resource Booking System.

import tkinter as tk
from gui.login_window import LoginWindow
from gui.lecturer_window import LecturerWindow
from gui.admin_window import AdminWindow
from gui.operator_window import OperatorWindow


def on_login_success(user):
    # Clears the window and opens the correct dashboard based on role
    for widget in root.winfo_children():
        widget.destroy()

    if user.role == "lecturer":
        LecturerWindow(root, user, on_logout)
    elif user.role == "admin":
        AdminWindow(root, user, on_logout)
    elif user.role == "operator":
        OperatorWindow(root, user, on_logout)
    else:
        print(f"Unknown role: {user.role}")


def on_logout():
    # Returns to the login screen
    for widget in root.winfo_children():
        widget.destroy()
    LoginWindow(root, on_login_success)


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root, on_login_success)
    root.mainloop()