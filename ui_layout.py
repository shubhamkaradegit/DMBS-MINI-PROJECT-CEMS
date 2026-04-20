import tkinter as tk
from tkinter import ttk


class EventUIBuilder:
    @staticmethod
    def button(parent, text, color, command, width=13):
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            width=width,
            bd=0,
            cursor="hand2",
            command=command,
        )

    @staticmethod
    def count_card(parent, title, value_var, value_color):
        frame = tk.Frame(parent, bg="#f8fcf9", bd=1, relief="solid")
        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#335542",
            padx=14,
            pady=4,
        ).pack()
        value_label = tk.Label(
            frame,
            textvariable=value_var,
            font=("Segoe UI", 16, "bold"),
            bg="#f8fcf9",
            fg=value_color,
            padx=14,
            pady=0,
        )
        value_label.pack(pady=(0, 6))
        return frame

    @staticmethod
    def build(app):
        header = tk.Frame(app.root, bg="#1f5faa", height=86)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="College Event Management System",
            font=("Times New Roman", 24, "bold"),
            bg="#1f5faa",
            fg="white",
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="Event Registration, Search, and Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#1f5faa",
            fg="#d8e9ff",
        )
        subtitle.pack()

        dashboard = tk.Frame(app.root, bg="#dce8e1", pady=8)
        dashboard.pack(fill="x")

        EventUIBuilder.count_card(
            dashboard, "Total Events", app.total_count_var, "#1f3a2c"
        ).pack(side="left", padx=8)
        EventUIBuilder.count_card(
            dashboard,
            "Upcoming Events",
            app.upcoming_count_var,
            "#165a3a",
        ).pack(side="left", padx=8)
        EventUIBuilder.count_card(
            dashboard, "Past Events", app.past_count_var, "#7a2e2e"
        ).pack(side="left", padx=8)

        body = tk.Frame(app.root, bg="#e9f1ee")
        body.pack(fill="both", expand=True, padx=12, pady=10)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left_panel = tk.Frame(body, bg="#e9f1ee")
        left_panel.grid(row=0, column=0, sticky="nsw", padx=(0, 10))

        form_frame = tk.LabelFrame(
            left_panel,
            text=" Event Form ",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fcf9",
            fg="#1f5faa",
            bd=2,
            relief="groove",
            padx=12,
            pady=10,
        )
        form_frame.pack(fill="x")

        tk.Label(
            form_frame,
            text="Event ID (Required)",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=0, column=0, sticky="w", pady=6)

        tk.Entry(
            form_frame,
            textvariable=app.var_event_id,
            font=("Segoe UI", 10),
            width=30,
            bd=1,
            relief="solid",
        ).grid(row=1, column=0, pady=(0, 8), sticky="w")

        tk.Label(
            form_frame,
            text="Event Name",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=2, column=0, sticky="w", pady=6)

        tk.Entry(
            form_frame,
            textvariable=app.var_event_name,
            font=("Segoe UI", 10),
            width=30,
            bd=1,
            relief="solid",
        ).grid(row=3, column=0, pady=(0, 8), sticky="w")

        tk.Label(
            form_frame,
            text="Date (DD-MM-YYYY)",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=4, column=0, sticky="w", pady=6)

        tk.Entry(
            form_frame,
            textvariable=app.var_event_date,
            font=("Segoe UI", 10),
            width=30,
            bd=1,
            relief="solid",
        ).grid(row=5, column=0, pady=(0, 8), sticky="w")

        tk.Label(
            form_frame,
            text="Venue",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=6, column=0, sticky="w", pady=6)

        tk.Entry(
            form_frame,
            textvariable=app.var_venue,
            font=("Segoe UI", 10),
            width=30,
            bd=1,
            relief="solid",
        ).grid(row=7, column=0, pady=(0, 8), sticky="w")

        tk.Label(
            form_frame,
            text="Enter Event ID manually",
            font=("Segoe UI", 9),
            bg="#f8fcf9",
            fg="#2f5f3f",
        ).grid(row=8, column=0, sticky="w", pady=(4, 0))

        form_btn_frame = tk.Frame(left_panel, bg="#e9f1ee")
        form_btn_frame.pack(fill="x", pady=(10, 0))

        EventUIBuilder.button(form_btn_frame, "Add Event", "#2ca25f", app.add_event).grid(
            row=0, column=0, padx=4, pady=4
        )
        EventUIBuilder.button(form_btn_frame, "Update", "#2b83ba", app.update_event).grid(
            row=0, column=1, padx=4, pady=4
        )
        EventUIBuilder.button(form_btn_frame, "Delete", "#d94841", app.delete_event).grid(
            row=0, column=2, padx=4, pady=4
        )
        EventUIBuilder.button(form_btn_frame, "Clear", "#6b7280", app.clear_form).grid(
            row=1, column=0, padx=4, pady=4
        )
        EventUIBuilder.button(form_btn_frame, "Export CSV", "#8a6c1d", app.export_csv).grid(
            row=1, column=1, padx=4, pady=4
        )
        EventUIBuilder.button(form_btn_frame, "Show All", "#6c5ce7", app.load_all_events).grid(
            row=1, column=2, padx=4, pady=4
        )

        right_panel = tk.Frame(body, bg="#e9f1ee")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        search_frame = tk.LabelFrame(
            right_panel,
            text=" Search and Filters ",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#1f5faa",
            bd=2,
            relief="groove",
            padx=10,
            pady=8,
        )
        search_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(
            search_frame,
            text="Search By",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=0, column=0, sticky="w", padx=4, pady=4)

        search_by_combo = ttk.Combobox(
            search_frame,
            textvariable=app.var_search_by,
            values=["Event Name", "Date", "Venue"],
            state="readonly",
            width=14,
        )
        search_by_combo.grid(row=0, column=1, padx=4, pady=4)

        tk.Entry(
            search_frame,
            textvariable=app.var_search_text,
            font=("Segoe UI", 10),
            width=26,
            bd=1,
            relief="solid",
        ).grid(row=0, column=2, padx=4, pady=4)

        EventUIBuilder.button(search_frame, "Search", "#2b83ba", app.search_events, width=11).grid(
            row=0, column=3, padx=4, pady=4
        )
        EventUIBuilder.button(
            search_frame, "Sort by Date", "#1d7a8c", app.sort_by_date, width=12
        ).grid(row=0, column=4, padx=4, pady=4)
        EventUIBuilder.button(
            search_frame, "Sort by Name", "#1d7a8c", app.sort_by_name, width=12
        ).grid(row=0, column=5, padx=4, pady=4)

        tk.Label(
            search_frame,
            text="Start Date",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).grid(row=1, column=0, sticky="w", padx=4, pady=4)

        tk.Entry(
            search_frame,
            textvariable=app.var_start_date,
            font=("Segoe UI", 10),
            width=16,
            bd=1,
            relief="solid",
        ).grid(row=1, column=1, padx=4, pady=4)

        end_date_frame = tk.Frame(search_frame, bg="#f8fcf9")
        end_date_frame.grid(row=1, column=2, columnspan=2, sticky="w", padx=4, pady=4)

        tk.Label(
            end_date_frame,
            text="End Date",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fcf9",
            fg="#274131",
        ).pack(side="left", padx=(0, 8))

        tk.Entry(
            end_date_frame,
            textvariable=app.var_end_date,
            font=("Segoe UI", 10),
            width=16,
            bd=1,
            relief="solid",
        ).pack(side="left")

        EventUIBuilder.button(
            search_frame,
            "Filter Date Range",
            "#3f6d49",
            app.filter_date_range,
            width=15,
        ).grid(row=1, column=4, padx=4, pady=4)
        EventUIBuilder.button(search_frame, "Reset", "#6b7280", app.reset_filters, width=12).grid(
            row=1, column=5, padx=4, pady=4
        )

        table_frame = tk.LabelFrame(
            right_panel,
            text=" Event Records (next 7 days highlighted) ",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fcf9",
            fg="#1f5faa",
            bd=2,
            relief="groove",
            padx=8,
            pady=8,
        )
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        columns = ("event_id", "event_name", "event_date", "venue")
        app.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        app.tree.heading("event_id", text="Event ID")
        app.tree.heading("event_name", text="Event Name")
        app.tree.heading("event_date", text="Date")
        app.tree.heading("venue", text="Venue")
        app.tree.column("event_id", width=110, anchor="center")
        app.tree.column("event_name", width=300, anchor="w")
        app.tree.column("event_date", width=140, anchor="center")
        app.tree.column("venue", width=250, anchor="w")
        app.tree.tag_configure("upcoming", background="#e6fff0")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=app.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=app.tree.xview)
        app.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        app.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        app.tree.bind("<<TreeviewSelect>>", app.on_row_select)

        status_bar = tk.Label(
            app.root,
            textvariable=app.var_status,
            font=("Segoe UI", 10),
            anchor="w",
            bg="#dce8e1",
            fg="#1f3a2c",
            padx=10,
            pady=6,
        )
        status_bar.pack(fill="x", side="bottom")
