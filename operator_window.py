# gui/operator_window.py
# Dashboard for system operators - full system-wide access.

import tkinter as tk
from tkinter import ttk
from database import get_connection
from reports import all_campuses_comparison


# Color constants (dark blue theme)
BG_COLOR     = "#dbeafe"   # light blue background
HEADER_BG    = "#172554"   # deep navy header (darker than admin)
BUTTON_BLUE  = "#2563eb"   # bright blue
BUTTON_GREEN = "#16a34a"   # green
BUTTON_RED   = "#dc2626"   # red
TEXT_COLOR   = "#172554"   # dark text


class OperatorWindow:
    # Main window for system operators

    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.build_ui()

    def build_ui(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(self.user.get_dashboard_title())
        self.root.geometry("1100x720")
        self.root.configure(bg=BG_COLOR)

        # ---- Header ----
        header = tk.Frame(self.root, bg=HEADER_BG, height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="System Operator - Institution Wide View",
            font=("Times New Roman", 15, "bold"),
            bg=HEADER_BG, fg="white"
        ).pack(side="left", padx=15, pady=12)
        tk.Button(
            header, text="Logout",
            command=self.on_logout,
            font=("Times New Roman", 11),
            bg=BUTTON_RED, fg="white",
            width=10, cursor="hand2"
        ).pack(side="right", padx=15, pady=12)

        # ---- Tabs ----
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.comparison_tab = tk.Frame(notebook, bg=BG_COLOR)
        self.bookings_tab = tk.Frame(notebook, bg=BG_COLOR)
        self.resources_tab = tk.Frame(notebook, bg=BG_COLOR)

        notebook.add(self.comparison_tab, text="  Cross-Campus Comparison  ")
        notebook.add(self.bookings_tab, text="  All Bookings  ")
        notebook.add(self.resources_tab, text="  All Resources  ")

        self.build_comparison_tab()
        self.build_bookings_tab()
        self.build_resources_tab()

    # --------------------------------------------------
    # Tab 1: Cross-Campus Comparison
    # --------------------------------------------------
    def build_comparison_tab(self):
        frame = tk.Frame(self.comparison_tab, bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            frame,
            text="Cross-Campus Usage Comparison",
            font=("Times New Roman", 14, "bold"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=8)

        tk.Label(
            frame,
            text="Compare resource usage, booking trends and campus-specific rules.",
            font=("Times New Roman", 10, "italic"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=(0, 10))

        # Table
        cols = ("Campus", "Total Resources", "Total Bookings",
                "Avg Duration (h)", "Most Used Resource")
        self.comparison_tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.comparison_tree.heading(c, text=c)
            self.comparison_tree.column(c, width=180, anchor="center")
        self.comparison_tree.pack(fill="both", expand=True, pady=10)

        tk.Button(
            frame, text="Generate Comparison",
            command=self.refresh_comparison,
            font=("Times New Roman", 11, "bold"),
            bg=BUTTON_GREEN, fg="white",
            width=25, cursor="hand2"
        ).pack(pady=8)

        self.refresh_comparison()

    def refresh_comparison(self):
        # Clears the table and reloads fresh stats for every campus
        for row in self.comparison_tree.get_children():
            self.comparison_tree.delete(row)

        data = all_campuses_comparison()
        for entry in data:
            self.comparison_tree.insert("", "end", values=(
                entry["campus_name"],
                entry["total_resources"],
                entry["total_bookings"],
                entry["average_duration"],
                entry["most_used_resource"]
            ))

    # --------------------------------------------------
    # Tab 2: All Bookings
    # --------------------------------------------------
    def build_bookings_tab(self):
        frame = tk.Frame(self.bookings_tab, bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            frame,
            text="All Bookings Across All Campuses",
            font=("Times New Roman", 14, "bold"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=8)

        cols = ("ID", "Campus", "Lecturer", "Resource",
                "Date", "Start", "Duration (h)", "Status")
        self.all_bookings_tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)
        for c in cols:
            self.all_bookings_tree.heading(c, text=c)
            self.all_bookings_tree.column(c, width=110, anchor="center")
        self.all_bookings_tree.pack(fill="both", expand=True, pady=10)

        tk.Button(
            frame, text="Refresh",
            command=self.refresh_all_bookings,
            font=("Times New Roman", 11),
            bg=BUTTON_BLUE, fg="white",
            width=15, cursor="hand2"
        ).pack(pady=5)

        self.refresh_all_bookings()

    def refresh_all_bookings(self):
        # Loads every booking in the system
        for row in self.all_bookings_tree.get_children():
            self.all_bookings_tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, c.name AS campus_name, u.username,
                   r.name AS resource_name, b.booking_date,
                   b.start_time, b.duration, b.status
            FROM bookings b
            JOIN campuses c ON b.campus_id = c.id
            JOIN users u ON b.user_id = u.id
            JOIN resources r ON b.resource_id = r.id
            ORDER BY b.booking_date DESC, b.start_time DESC
        """)
        for r in cursor.fetchall():
            self.all_bookings_tree.insert("", "end", values=(
                r["id"], r["campus_name"], r["username"], r["resource_name"],
                r["booking_date"], r["start_time"], r["duration"],
                r["status"].capitalize()
            ))
        conn.close()

    # --------------------------------------------------
    # Tab 3: All Resources
    # --------------------------------------------------
    def build_resources_tab(self):
        frame = tk.Frame(self.resources_tab, bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            frame,
            text="All Resources Across All Campuses",
            font=("Times New Roman", 14, "bold"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=8)

        cols = ("ID", "Campus", "Name", "Type", "Capacity")
        self.all_resources_tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)
        for c in cols:
            self.all_resources_tree.heading(c, text=c)
            self.all_resources_tree.column(c, width=160, anchor="center")
        self.all_resources_tree.pack(fill="both", expand=True, pady=10)

        tk.Button(
            frame, text="Refresh",
            command=self.refresh_all_resources,
            font=("Times New Roman", 11),
            bg=BUTTON_BLUE, fg="white",
            width=15, cursor="hand2"
        ).pack(pady=5)

        self.refresh_all_resources()

    def refresh_all_resources(self):
        # Loads every resource in the system
        for row in self.all_resources_tree.get_children():
            self.all_resources_tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, c.name AS campus_name, r.name, r.type, r.capacity
            FROM resources r
            JOIN campuses c ON r.campus_id = c.id
            ORDER BY c.name, r.name
        """)
        for r in cursor.fetchall():
            self.all_resources_tree.insert("", "end", values=(
                r["id"], r["campus_name"], r["name"],
                r["type"], r["capacity"]
            ))
        conn.close()