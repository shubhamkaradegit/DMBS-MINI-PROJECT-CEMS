from datetime import datetime

try:
    import oracledb
except ImportError:
    oracledb = None


class EventRepository:
    def __init__(self, user, password, dsn, client_lib_dir=""):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.client_lib_dir = client_lib_dir
        self.conn = None
        self.cursor = None

    def connect(self):
        if oracledb is None:
            raise RuntimeError("Oracle driver is not installed. Install using: pip install oracledb")

        if self.client_lib_dir:
            try:
                oracledb.init_oracle_client(lib_dir=self.client_lib_dir)
            except Exception as exc:
                # Ignore the error if client is already initialized.
                if "DPY-2019" not in str(exc):
                    raise

        self.conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def add_event(self, event_id, event_name, event_date, venue):
        self.cursor.execute(
            """
            INSERT INTO events (event_id, event_name, event_date, venue)
            VALUES (:1, :2, :3, :4)
            """,
            (event_id, event_name, event_date, venue),
        )
        self.conn.commit()
        return event_id

    def update_event(self, event_id, event_name, event_date, venue):
        self.cursor.execute(
            """
            UPDATE events
            SET event_name = :1,
                event_date = :2,
                venue = :3
            WHERE event_id = :4
            """,
            (event_name, event_date, venue, event_id),
        )
        self.conn.commit()
        return self.cursor.rowcount

    def delete_event(self, event_id):
        self.cursor.execute("DELETE FROM events WHERE event_id = :1", (event_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def fetch_all_events(self):
        self.cursor.execute(
            """
            SELECT event_id, event_name, event_date, venue
            FROM events
            ORDER BY event_date, event_id
            """
        )
        return self.cursor.fetchall()

    def fetch_sorted_events(self, order_clause):
        self.cursor.execute(
            f"""
            SELECT event_id, event_name, event_date, venue
            FROM events
            ORDER BY {order_clause}
            """
        )
        return self.cursor.fetchall()

    def search_by_name(self, search_text):
        self.cursor.execute(
            """
            SELECT event_id, event_name, event_date, venue
            FROM events
            WHERE UPPER(event_name) LIKE UPPER(:1)
            ORDER BY event_date, event_id
            """,
            (f"%{search_text}%",),
        )
        return self.cursor.fetchall()

    def search_by_venue(self, search_text):
        self.cursor.execute(
            """
            SELECT event_id, event_name, event_date, venue
            FROM events
            WHERE UPPER(venue) LIKE UPPER(:1)
            ORDER BY event_date, event_id
            """,
            (f"%{search_text}%",),
        )
        return self.cursor.fetchall()

    def search_by_date(self, parsed_date):
        self.cursor.execute(
            """
            SELECT event_id, event_name, event_date, venue
            FROM events
            WHERE TRUNC(event_date) = TRUNC(:1)
            ORDER BY event_date, event_id
            """,
            (parsed_date,),
        )
        return self.cursor.fetchall()

    def filter_by_date_range(self, start_date, end_date):
        self.cursor.execute(
            """
            SELECT event_id, event_name, event_date, venue
            FROM events
            WHERE TRUNC(event_date) BETWEEN TRUNC(:1) AND TRUNC(:2)
            ORDER BY event_date, event_id
            """,
            (start_date, end_date),
        )
        return self.cursor.fetchall()

    def get_dashboard_counts(self):
        self.cursor.execute("SELECT COUNT(*) FROM events")
        total_events = int(self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) FROM events WHERE TRUNC(event_date) >= TRUNC(SYSDATE)")
        upcoming_events = int(self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) FROM events WHERE TRUNC(event_date) < TRUNC(SYSDATE)")
        past_events = int(self.cursor.fetchone()[0])

        return total_events, upcoming_events, past_events

    @staticmethod
    def is_dpy_3010_error(exc):
        return "DPY-3010" in str(exc)

    @staticmethod
    def is_duplicate_id_error(exc):
        return "ORA-00001" in str(exc)

    @staticmethod
    def format_error(exc):
        return str(exc)

    @staticmethod
    def now_date():
        return datetime.now().date()
