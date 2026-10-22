# gui/login_window.py
# Login screen - the first window the user sees.

import tkinter as tk
from tkinter import messagebox, ttk
from auth import login_user, register_user
from database import get_connection


# Color constants (dark blue theme)
BG_COLOR    = "#dbeafe"   # light blue background
HEADER_BG   = "#1e3a8a"   # deep navy
BUTTON_BLUE = "#2563eb"   # bright blue
BUTTON_GREEN= "#16a34a"   # green
TEXT_COLOR  = "#172554"   # dark text


class LoginWindow:
    # Login screen for all users

    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        self.root.title("Smart Campus Resource Booking - Login")
        self.root.geometry("480x420")
        self.root.configure(bg=BG_COLOR)
        self.build_ui()

    def build_ui(self):
        # Clear any existing widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top header bar
        header = tk.Frame(self.root, bg=HEADER_BG, height=80)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Smart Campus Booking System",
            font=("Times New Roman", 16, "bold"),
            bg=HEADER_BG, fg="white"
        ).pack(pady=20)

        # Subtitle
        tk.Label(
            self.root,
            text="Richfield Graduate Institution",
            font=("Times New Roman", 11, "italic"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=10)

        # Login form container
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Times New Roman", 12), bg=BG_COLOR, fg=TEXT_COLOR)\
            .grid(row=0, column=0, sticky="e", pady=8, padx=5)
        self.username_entry = tk.Entry(frame, font=("Times New Roman", 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(frame, text="Password:", font=("Times New Roman", 12), bg=BG_COLOR, fg=TEXT_COLOR)\
            .grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.password_entry = tk.Entry(frame, show="*", font=("Times New Roman", 12), width=25)
        self.password_entry.grid(row=1, column=1, pady=8, padx=5)

        # Login button
        tk.Button(
            self.root,
            text="Login",
            command=self.login,
            font=("Times New Roman", 12, "bold"),
            bg=BUTTON_BLUE, fg="white",
            width=18, cursor="hand2"
        ).pack(pady=15)

        # Register button (for lecturers only)
        tk.Button(
            self.root,
            text="Register as Lecturer",
            command=self.open_register,
            font=("Times New Roman", 11),
            bg=BUTTON_GREEN, fg="white",
            width=22, cursor="hand2"
        ).pack(pady=5)

    def login(self):
        # Called when the user clicks Login
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        user = login_user(username, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_register(self):
        # Opens the register popup window
        RegisterWindow(self.root, self.build_ui)


class RegisterWindow:
    # Popup that lets a lecturer create a new account

    def __init__(self, parent, on_close):
        self.parent = parent
        self.on_close = on_close

        self.win = tk.Toplevel(parent)
        self.win.title("Register Lecturer")
        self.win.geometry("420x380")
        self.win.configure(bg=BG_COLOR)
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.win, bg=HEADER_BG, height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Register New Lecturer",
            font=("Times New Roman", 14, "bold"),
            bg=HEADER_BG, fg="white"
        ).pack(pady=15)

        frame = tk.Frame(self.win, bg=BG_COLOR)
        frame.pack(pady=15)

        # Username
        tk.Label(frame, text="Username:", font=("Times New Roman", 12), bg=BG_COLOR, fg=TEXT_COLOR)\
            .grid(row=0, column=0, sticky="e", pady=8, padx=5)
        self.username_entry = tk.Entry(frame, font=("Times New Roman", 12), width=22)
        self.username_entry.grid(row=0, column=1, pady=8, padx=5)

        # Password
        tk.Label(frame, text="Password:", font=("Times New Roman", 12), bg=BG_COLOR, fg=TEXT_COLOR)\
            .grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.password_entry = tk.Entry(frame, show="*", font=("Times New Roman", 12), width=22)
        self.password_entry.grid(row=1, column=1, pady=8, padx=5)

        # Campus selection
        tk.Label(frame, text="Campus:", font=("Times New Roman", 12), bg=BG_COLOR, fg=TEXT_COLOR)\
            .grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.campus_combo = ttk.Combobox(frame, font=("Times New Roman", 12), width=20)
        self.campus_combo.grid(row=2, column=1, pady=8, padx=5)
        self.load_campuses()

        # Register button
        tk.Button(
            self.win,
            text="Register",
            command=self.register,
            font=("Times New Roman", 12, "bold"),
            bg=BUTTON_GREEN, fg="white",
            width=15, cursor="hand2"
        ).pack(pady=20)

    def load_campuses(self):
        # Loads all campuses into the dropdown
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM campuses ORDER BY name")
        self.campuses = cursor.fetchall()
        conn.close()

        self.campus_combo["values"] = [c["name"] for c in self.campuses]
        if self.campuses:
            self.campus_combo.current(0)

    def register(self):
        # Called when the user clicks Register
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        campus_name = self.campus_combo.get()

        if not username or not password or not campus_name:
            messagebox.showerror("Error", "All fields are required.")
            return

        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return

        # Find the campus id for the selected campus
        campus_id = None
        for c in self.campuses:
            if c["name"] == campus_name:
                campus_id = c["id"]
                break

        success, msg = register_user(username, password, "lecturer", campus_id)

        if success:
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            self.win.destroy()
            self.on_close()
        else:
            messagebox.showerror("Error", msg)