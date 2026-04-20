import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    import oracledb as cx_Oracle
except ImportError:
    cx_Oracle = None


# -----------------------------
# Update these with your Oracle 11g credentials
# -----------------------------
ORACLE_USER = "system"
ORACLE_PASSWORD = "123456"
ORACLE_DSN = "localhost:1521/XE"
# Required for Oracle 11g: set this to your Instant Client folder path.
# Example: r"C:\\oracle\\instantclient_19_22"
ORACLE_CLIENT_LIB_DIR = r"C:\oraclexe\app\oracle\product\11.2.0\server\bin"


class EventManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Event Management System")
        self.root.geometry("1180x730")
        self.root.configure(bg="#e9f1ee")

        self.conn = None
        self.cursor = None

        self.var_event_id = tk.StringVar()
        self.var_event_name = tk.StringVar()
        self.var_event_date = tk.StringVar()
        self.var_venue = tk.StringVar()
        self.var_status = tk.StringVar(value="Ready")

        self.build_ui()
        self.connect_db()
        self.load_all_events()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#4f8a5b", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="College Event Management System",
            font=("Times New Roman", 24, "bold"),
            bg="#4f8a5b",
            fg="white",
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="Event Registration and Records",
            font=("Segoe UI", 11, "bold"),
            bg="#4f8a5b",
            fg="#d9f3df",
        )
        subtitle.pack()

        body = tk.Frame(self.root, bg="#e9f1ee")
        body.pack(fill="both", expand=True, padx=14, pady=12)

        form_frame = tk.LabelFrame(
            body,
            text=" Event Details ",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fcf9",
            fg="#3f6d49",
            bd=2,
            relief="groove",
            padx=14,
            pady=12,
        )
        form_frame.pack(fill="x")

        tk.Label(
            form_frame,
            text="Event ID",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=8)

        tk.Entry(
            form_frame,
            textvariable=self.var_event_id,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=28,
        ).grid(row=0, column=1, padx=8, pady=8)

        tk.Label(
            form_frame,
            text="Event Name",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=0, column=2, sticky="w", padx=8, pady=8)

        tk.Entry(
            form_frame,
            textvariable=self.var_event_name,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=40,
        ).grid(row=0, column=3, padx=8, pady=8)

        tk.Label(
            form_frame,
            text="Date (DD-MM-YYYY)",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=1, column=0, sticky="w", padx=8, pady=8)

        tk.Entry(
            form_frame,
            textvariable=self.var_event_date,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=28,
        ).grid(row=1, column=1, padx=8, pady=8)

        tk.Label(
            form_frame,
            text="Venue",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=1, column=2, sticky="w", padx=8, pady=8)

        tk.Entry(
            form_frame,
            textvariable=self.var_venue,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=40,
        ).grid(row=1, column=3, padx=8, pady=8)

        button_frame = tk.Frame(body, bg="#e9f1ee")
        button_frame.pack(fill="x", pady=(12, 8))

        tk.Button(
            button_frame,
            text="Add Event",
            font=("Segoe UI", 10, "bold"),
            bg="#2ca25f",
            fg="white",
            activebackground="#258c53",
            activeforeground="white",
            width=14,
            bd=0,
            cursor="hand2",
            command=self.add_event,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Update",
            font=("Segoe UI", 10, "bold"),
            bg="#2b83ba",
            fg="white",
            activebackground="#216a97",
            activeforeground="white",
            width=14,
            bd=0,
            cursor="hand2",
            command=self.update_event,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            font=("Segoe UI", 10, "bold"),
            bg="#d94841",
            fg="white",
            activebackground="#b23934",
            activeforeground="white",
            width=14,
            bd=0,
            cursor="hand2",
            command=self.delete_event,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="View All",
            font=("Segoe UI", 10, "bold"),
            bg="#6c5ce7",
            fg="white",
            activebackground="#5a4cc3",
            activeforeground="white",
            width=14,
            bd=0,
            cursor="hand2",
            command=self.load_all_events,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Clear Form",
            font=("Segoe UI", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=14,
            bd=0,
            cursor="hand2",
            command=self.clear_form,
        ).pack(side="left", padx=5)

        table_frame = tk.LabelFrame(
            body,
            text=" Event Records ",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fcf9",
            fg="#3f6d49",
            bd=2,
            relief="groove",
            padx=8,
            pady=8,
        )
        table_frame.pack(fill="both", expand=True, pady=(6, 0))

        columns = ("event_id", "event_name", "event_date", "venue")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("event_id", text="Event ID")
        self.tree.heading("event_name", text="Event Name")
        self.tree.heading("event_date", text="Date")
        self.tree.heading("venue", text="Venue")

        self.tree.column("event_id", width=120, anchor="center")
        self.tree.column("event_name", width=360, anchor="w")
        self.tree.column("event_date", width=170, anchor="center")
        self.tree.column("venue", width=300, anchor="w")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        status_bar = tk.Label(
            self.root,
            textvariable=self.var_status,
            font=("Segoe UI", 10),
            anchor="w",
            bg="#dce8e1",
            fg="#1f3a2c",
            padx=10,
            pady=6,
        )
        status_bar.pack(fill="x", side="bottom")

    def connect_db(self):
        if cx_Oracle is None:
            messagebox.showerror(
                "Missing Dependency",
                "Oracle driver is not installed. Install it using: pip install oracledb",
            )
            self.var_status.set("Database library missing: install oracledb")
            return

        try:
            if ORACLE_CLIENT_LIB_DIR:
                cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_LIB_DIR)

            self.conn = cx_Oracle.connect(
                user=ORACLE_USER,
                password=ORACLE_PASSWORD,
                dsn=ORACLE_DSN,
            )
            self.cursor = self.conn.cursor()
            self.var_status.set("Connected to Oracle successfully")
        except Exception as exc:
            err_text = str(exc)
            if "DPY-3010" in err_text:
                messagebox.showerror(
                    "Database Connection Error",
                    "Oracle 11g requires thick mode.\n\n"
                    "1) Download Oracle Instant Client (64-bit).\n"
                    "2) Set ORACLE_CLIENT_LIB_DIR in this file.\n"
                    "3) Restart and run the app again.\n\n"
                    f"Original error:\n{err_text}",
                )
                self.var_status.set("DPY-3010: configure Instant Client for Oracle 11g")
            else:
                messagebox.showerror("Database Connection Error", err_text)
                self.var_status.set("Connection failed. Check credentials, DSN, and listener")

    def validate_inputs(self):
        event_id = self.var_event_id.get().strip()
        event_name = self.var_event_name.get().strip()
        event_date = self.var_event_date.get().strip()
        venue = self.var_venue.get().strip()

        if not event_id or not event_name or not event_date or not venue:
            messagebox.showwarning("Missing Data", "Please fill all input fields.")
            return None

        if not event_id.isdigit():
            messagebox.showwarning("Invalid Event ID", "Event ID must be a number.")
            return None

        try:
            parsed_date = datetime.strptime(event_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Date must be in DD-MM-YYYY format.",
            )
            return None

        return int(event_id), event_name, parsed_date, venue

    def add_event(self):
        if self.cursor is None:
            messagebox.showerror("Database Error", "No Oracle connection available.")
            return

        validated = self.validate_inputs()
        if not validated:
            return

        event_id, event_name, parsed_date, venue = validated

        try:
            self.cursor.execute(
                """
                INSERT INTO events (event_id, event_name, event_date, venue)
                VALUES (:1, :2, :3, :4)
                """,
                (event_id, event_name, parsed_date, venue),
            )
            self.conn.commit()
            self.load_all_events()
            self.var_status.set(f"Added event ID {event_id}")
            messagebox.showinfo("Success", "Event added successfully.")
            self.clear_form()
        except cx_Oracle.IntegrityError:
            messagebox.showerror(
                "Duplicate Event ID",
                "This Event ID already exists. Use a different ID.",
            )
        except Exception as exc:
            messagebox.showerror("Insert Error", str(exc))

    def update_event(self):
        if self.cursor is None:
            messagebox.showerror("Database Error", "No Oracle connection available.")
            return

        validated = self.validate_inputs()
        if not validated:
            return

        event_id, event_name, parsed_date, venue = validated

        try:
            self.cursor.execute(
                """
                UPDATE events
                SET event_name = :1,
                    event_date = :2,
                    venue = :3
                WHERE event_id = :4
                """,
                (event_name, parsed_date, venue, event_id),
            )

            if self.cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "No event found with this Event ID.")
                return

            self.conn.commit()
            self.load_all_events()
            self.var_status.set(f"Updated event ID {event_id}")
            messagebox.showinfo("Success", "Event updated successfully.")
            self.clear_form()
        except Exception as exc:
            messagebox.showerror("Update Error", str(exc))

    def delete_event(self):
        if self.cursor is None:
            messagebox.showerror("Database Error", "No Oracle connection available.")
            return

        event_id = self.var_event_id.get().strip()
        if not event_id:
            messagebox.showwarning("Missing Event ID", "Enter Event ID to delete.")
            return

        if not event_id.isdigit():
            messagebox.showwarning("Invalid Event ID", "Event ID must be numeric.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete event ID {event_id}?",
        )
        if not confirm:
            return

        try:
            self.cursor.execute("DELETE FROM events WHERE event_id = :1", (int(event_id),))

            if self.cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "No event found with this Event ID.")
                return

            self.conn.commit()
            self.load_all_events()
            self.var_status.set(f"Deleted event ID {event_id}")
            messagebox.showinfo("Success", "Event deleted successfully.")
            self.clear_form()
        except Exception as exc:
            messagebox.showerror("Delete Error", str(exc))

    def load_all_events(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.cursor is None:
            return

        try:
            self.cursor.execute(
                """
                SELECT event_id,
                       event_name,
                       TO_CHAR(event_date, 'DD-MM-YYYY') AS event_date,
                       venue
                FROM events
                ORDER BY event_date, event_id
                """
            )
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)

            self.var_status.set(f"Loaded {len(rows)} event record(s)")
        except Exception as exc:
            messagebox.showerror("Fetch Error", str(exc))

    def on_row_select(self, _event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        self.var_event_id.set(values[0])
        self.var_event_name.set(values[1])
        self.var_event_date.set(values[2])
        self.var_venue.set(values[3])

    def clear_form(self):
        self.var_event_id.set("")
        self.var_event_name.set("")
        self.var_event_date.set("")
        self.var_venue.set("")

    def close_app(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
