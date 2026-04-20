import csv
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, ttk

from config import (
    ORACLE_CLIENT_LIB_DIR,
    ORACLE_DSN,
    ORACLE_PASSWORD,
    ORACLE_USER,
    PREVENT_PAST_DATES,
)
from event_repository import EventRepository
from ui_layout import EventUIBuilder


class EventManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Event Management System")
        self.root.geometry("1280x780")
        self.root.configure(bg="#e9f1ee")

        self.repo = EventRepository(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            client_lib_dir=ORACLE_CLIENT_LIB_DIR,
        )

        self.var_event_id = tk.StringVar()
        self.var_event_name = tk.StringVar()
        self.var_event_date = tk.StringVar()
        self.var_venue = tk.StringVar()
        self.var_search_text = tk.StringVar()
        self.var_search_by = tk.StringVar(value="Event Name")
        self.var_start_date = tk.StringVar()
        self.var_end_date = tk.StringVar()
        self.var_status = tk.StringVar(value="Ready")

        self.total_count_var = tk.StringVar(value="0")
        self.upcoming_count_var = tk.StringVar(value="0")
        self.past_count_var = tk.StringVar(value="0")

        self.build_ui()
        self.connect_db()
        self.load_all_events()

    def build_ui(self):
        EventUIBuilder.build(self)

    def connect_db(self):
        try:
            self.repo.connect()
            self.var_status.set("Connected to Oracle successfully")
        except Exception as exc:
            err_text = EventRepository.format_error(exc)
            if EventRepository.is_dpy_3010_error(exc):
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

    def parse_date(self, date_text):
        try:
            return datetime.strptime(date_text.strip(), "%d-%m-%Y")
        except ValueError:
            return None

    def validate_event_payload(self, require_id=False):
        event_id = self.var_event_id.get().strip()
        event_name = self.var_event_name.get().strip()
        event_date_text = self.var_event_date.get().strip()
        venue = self.var_venue.get().strip()

        if require_id and not event_id:
            messagebox.showwarning("Missing Event ID", "Event ID is required for this action.")
            return None

        if require_id and not event_id.isdigit():
            messagebox.showwarning("Invalid Event ID", "Event ID must be numeric.")
            return None

        if not event_name or not event_date_text or not venue:
            messagebox.showwarning("Missing Data", "Please fill Event Name, Date, and Venue.")
            return None

        event_date = self.parse_date(event_date_text)
        if event_date is None:
            messagebox.showwarning("Invalid Date", "Date must be in DD-MM-YYYY format.")
            return None

        if PREVENT_PAST_DATES and event_date.date() < datetime.now().date():
            messagebox.showwarning(
                "Invalid Date",
                "Past dates are not allowed for new or updated events.",
            )
            return None

        event_id_num = int(event_id) if event_id else None
        return event_id_num, event_name, event_date, venue

    def add_event(self):
        if self.repo.cursor is None:
            messagebox.showerror("Database Error", "No Oracle connection available.")
            return

        validated = self.validate_event_payload(require_id=True)
        if not validated:
            return

        event_id, event_name, event_date, venue = validated

        try:
            new_id = self.repo.add_event(event_id, event_name, event_date, venue)
            self.load_all_events()
            self.var_status.set(f"Added event ID {new_id}")
            messagebox.showinfo("Success", f"Event added successfully with ID {new_id}.")
            self.clear_form()
        except Exception as exc:
            err_text = EventRepository.format_error(exc)
            if EventRepository.is_duplicate_id_error(exc):
                messagebox.showerror(
                    "Insert Error",
                    "Event ID already exists. Please use a unique Event ID.",
                )
            else:
                messagebox.showerror("Insert Error", err_text)

    def update_event(self):
        if self.repo.cursor is None:
            messagebox.showerror("Database Error", "No Oracle connection available.")
            return

        validated = self.validate_event_payload(require_id=True)
        if not validated:
            return

        event_id, event_name, event_date, venue = validated

        try:
            affected_rows = self.repo.update_event(event_id, event_name, event_date, venue)

            if affected_rows == 0:
                messagebox.showwarning("Not Found", "No event found with this Event ID.")
                return

            self.load_all_events()
            self.var_status.set(f"Updated event ID {event_id}")
            messagebox.showinfo("Success", "Event updated successfully.")
            self.clear_form()
        except Exception as exc:
            messagebox.showerror("Update Error", str(exc))

    def delete_event(self):
        if self.repo.cursor is None:
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
            affected_rows = self.repo.delete_event(int(event_id))
            if affected_rows == 0:
                messagebox.showwarning("Not Found", "No event found with this Event ID.")
                return

            self.load_all_events()
            self.var_status.set(f"Deleted event ID {event_id}")
            messagebox.showinfo("Success", "Event deleted successfully.")
            self.clear_form()
        except Exception as exc:
            messagebox.showerror("Delete Error", str(exc))

    def _render_rows(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        for event_id, event_name, event_date, venue in rows:
            date_str = event_date.strftime("%d-%m-%Y") if event_date else ""
            tags = ()
            if event_date and today <= event_date.date() <= next_week:
                tags = ("upcoming",)

            self.tree.insert(
                "",
                "end",
                values=(event_id, event_name, date_str, venue),
                tags=tags,
            )

    def refresh_dashboard(self):
        if self.repo.cursor is None:
            return

        total_events, upcoming_events, past_events = self.repo.get_dashboard_counts()

        self.total_count_var.set(str(total_events))
        self.upcoming_count_var.set(str(upcoming_events))
        self.past_count_var.set(str(past_events))

    def load_all_events(self):
        if self.repo.cursor is None:
            return

        try:
            rows = self.repo.fetch_all_events()
            self._render_rows(rows)
            self.refresh_dashboard()
            self.var_status.set(f"Loaded {len(rows)} event record(s)")
        except Exception as exc:
            messagebox.showerror("Fetch Error", str(exc))

    def sort_by_date(self):
        self.load_sorted("event_date, event_id", "Sorted by date")

    def sort_by_name(self):
        self.load_sorted("UPPER(event_name), event_id", "Sorted by name")

    def load_sorted(self, order_clause, status_text):
        if self.repo.cursor is None:
            return

        try:
            rows = self.repo.fetch_sorted_events(order_clause)
            self._render_rows(rows)
            self.refresh_dashboard()
            self.var_status.set(f"{status_text}. {len(rows)} record(s) shown")
        except Exception as exc:
            messagebox.showerror("Sort Error", str(exc))

    def search_events(self):
        if self.repo.cursor is None:
            return

        search_text = self.var_search_text.get().strip()
        if not search_text:
            messagebox.showwarning("Missing Input", "Enter a value for search.")
            return

        search_by = self.var_search_by.get()

        try:
            if search_by == "Event Name":
                rows = self.repo.search_by_name(search_text)
            elif search_by == "Venue":
                rows = self.repo.search_by_venue(search_text)
            else:
                parsed_date = self.parse_date(search_text)
                if parsed_date is None:
                    messagebox.showwarning("Invalid Date", "Use DD-MM-YYYY for date search.")
                    return
                rows = self.repo.search_by_date(parsed_date)

            self._render_rows(rows)
            self.refresh_dashboard()
            self.var_status.set(f"Search result: {len(rows)} record(s)")
        except Exception as exc:
            messagebox.showerror("Search Error", str(exc))

    def filter_date_range(self):
        if self.repo.cursor is None:
            return

        start_text = self.var_start_date.get().strip()
        end_text = self.var_end_date.get().strip()

        if not start_text or not end_text:
            messagebox.showwarning("Missing Input", "Enter both start and end dates.")
            return

        start_date = self.parse_date(start_text)
        end_date = self.parse_date(end_text)

        if start_date is None or end_date is None:
            messagebox.showwarning("Invalid Date", "Date range must be DD-MM-YYYY.")
            return

        if start_date > end_date:
            messagebox.showwarning("Invalid Range", "Start date cannot be after end date.")
            return

        try:
            rows = self.repo.filter_by_date_range(start_date, end_date)
            self._render_rows(rows)
            self.refresh_dashboard()
            self.var_status.set(f"Date range filter: {len(rows)} record(s)")
        except Exception as exc:
            messagebox.showerror("Filter Error", str(exc))

    def reset_filters(self):
        self.var_search_text.set("")
        self.var_start_date.set("")
        self.var_end_date.set("")
        self.load_all_events()

    def export_csv(self):
        rows = [self.tree.item(item, "values") for item in self.tree.get_children()]
        if not rows:
            messagebox.showwarning("No Data", "No rows available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Event Records",
        )
        if not file_path:
            return

        try:
            csv_rows = []
            for row in rows:
                event_id, event_name, date_text, venue = row

                # Force date as text so Excel does not auto-format it as #######
                # when the column is narrow or locale parsing differs.
                safe_date = date_text
                try:
                    datetime.strptime(str(date_text), "%d-%m-%Y")
                    safe_date = f"'{date_text}"
                except ValueError:
                    pass

                csv_rows.append([event_id, event_name, safe_date, venue])

            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Event ID", "Event Name", "Date", "Venue"])
                writer.writerows(csv_rows)

            self.var_status.set(f"Exported {len(rows)} row(s) to CSV")
            messagebox.showinfo("Export Complete", "CSV exported successfully.")
        except Exception as exc:
            messagebox.showerror("Export Error", str(exc))

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
            self.repo.close()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
