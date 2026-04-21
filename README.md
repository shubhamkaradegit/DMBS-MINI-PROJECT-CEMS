# College Event Management System
## Tkinter Desktop Application + Oracle 11g Database

---

## 📋 Project Overview

The **College Event Management System** is a desktop application built with **Python (Tkinter)** and **Oracle 11g Database**. It allows users to efficiently manage college events with full CRUD (Create, Read, Update, Delete) functionality, search capabilities, filtering, and dashboard statistics.

### Key Features:
- ✅ **CRUD Operations**: Add, View, Edit, and Delete events
- ✅ **Search Functionality**: Find events by name, venue, or date
- ✅ **Date Filtering**: Filter events within a date range
- ✅ **Dashboard Stats**: View total, upcoming, and past events
- ✅ **Data Validation**: Prevent invalid dates and incomplete data
- ✅ **CSV Export**: Export event data to CSV files
- ✅ **User-Friendly UI**: Clean, intuitive interface with Tkinter
- ✅ **Professional UI Highlights**: Upcoming events (next 7 days) highlighted in the table

---

## 📁 Project Structure

```
college_event_management/
├── college_event_management.py    # Main application - UI controller & business logic
├── event_repository.py             # Database layer - All SQL queries & Oracle operations
├── ui_layout.py                    # Tkinter UI components & layout
├── config.py                       # Database credentials & configuration
├── sql_queries.sql                 # ALL SQL code used in the project (NEW)
├── schema.sql                      # Original table creation script (reference)
├── upgrade_existing_schema.sql     # Original upgrade script (reference)
├── README.md                       # This file
└── .venv/                          # Python virtual environment
```

### File Descriptions:

| File | Purpose |
|------|---------|
| **college_event_management.py** | Main application controller. Manages UI interactions, validation, event handling, and coordinates with the database layer. |
| **event_repository.py** | Database abstraction layer. Contains all SQL queries and Oracle database operations. |
| **ui_layout.py** | Tkinter UI builder. Defines all buttons, labels, text fields, tables, and layout organization. |
| **config.py** | Configuration file. Stores Oracle credentials, DSN, and Instant Client path. |
| **sql_queries.sql** | ⭐ **CONSOLIDATED SQL FILE** - Contains ALL SQL queries used in the project (table creation, indexes, CRUD operations, searches, and statistics). |
| **schema.sql** | Original schema creation script (for reference). Superseded by sql_queries.sql. |
| **upgrade_existing_schema.sql** | Original upgrade script (for reference). Superseded by sql_queries.sql. |

---

## 🗄️ Database Schema

### Table: `events`

```sql
CREATE TABLE events (
    event_id     NUMBER PRIMARY KEY,
    event_name   VARCHAR2(120) NOT NULL,
    event_date   DATE NOT NULL,
    venue        VARCHAR2(120) NOT NULL,
    created_at   DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT chk_event_date CHECK (event_date >= TRUNC(SYSDATE))
);
```

### Indexes (for performance optimization):
- `idx_events_date` - Index on event_date
- `idx_events_name` - Index on event_name
- `idx_events_venue` - Index on venue

### Constraints:
- **Primary Key**: event_id (unique identifier)
- **Check Constraint**: event_date must be today or in the future (prevents past dates)

---

## 💾 SQL Queries Summary

### **ALL SQL queries used in the project are in `sql_queries.sql`**

The following queries are included:

#### **Table & Index Creation**
1. `CREATE TABLE events` - Define the events table structure
2. `CREATE INDEX` statements - Create 3 indexes for better performance

#### **CRUD Operations**
3. `INSERT INTO events` - Add new event
4. `UPDATE events` - Modify existing event
5. `DELETE FROM events` - Remove event

#### **Read Operations**
6. `SELECT * FROM events ORDER BY event_date` - Fetch all events
7. `SELECT * FROM events ORDER BY {order_clause}` - Fetch with custom sorting

#### **Search Queries**
8. Search by Event Name (case-insensitive LIKE match)
9. Search by Venue (case-insensitive LIKE match)
10. Search by Exact Date (TRUNC function for date comparison)
11. Filter by Date Range (BETWEEN clause)

#### **Dashboard Statistics**
12. Count total events
13. Count upcoming events (date >= today)
14. Count past events (date < today)

**Total: 14+ SQL operations** - All documented with parameters and purpose in `sql_queries.sql`.

---

## 🚀 Installation & Setup

### Step 1: Install Python Dependencies

```bash
pip install oracledb
```

### Step 2: Configure Oracle Connection

**For Oracle 11g (Thick Mode Required):**

1. Download **Oracle Instant Client** (64-bit) from [Oracle website](https://www.oracle.com/database/technologies/instant-client/downloads.html)
   - Example: `oracle/instantclient_19_22`

2. Extract the downloaded file to a folder (e.g., `C:\oracle\instantclient_19_22`)

3. Open `config.py` and update:
   ```python
   ORACLE_CLIENT_LIB_DIR = r"C:\oracle\instantclient_19_22"  # Your path
   ORACLE_USER = "your_username"      # Oracle username
   ORACLE_PASSWORD = "your_password"  # Oracle password
   ORACLE_DSN = "localhost:1521/XE"   # Your Oracle DSN
   ```

   **Example DSN values:**
   - `localhost:1521/XE` - Oracle Express Edition
   - `localhost:1521/ORCL` - Standard Oracle Database

### Step 3: Create Database Table

1. Open **SQL*Plus** or **SQL Developer**
2. Connect to your Oracle 11g database
3. Run **`sql_queries.sql`** (it contains all necessary SQL)

   **OR** if table already exists:
   - Run the upgrade section in `sql_queries.sql` to add missing constraints/indexes

### Step 4: Run the Application

```bash
python college_event_management.py
```

---

## 🎯 How to Use the Application

### **Main Menu Options**

| Operation | Steps |
|-----------|-------|
| **Add Event** | 1. Enter Event ID (unique) 2. Enter Event Name 3. Select Event Date (DD-MM-YYYY) 4. Enter Venue 5. Click "Add Event" |
| **Update Event** | 1. Click any row in the table to auto-fill form 2. Modify fields as needed 3. Click "Update Event" |
| **Delete Event** | 1. Click any row in the table 2. Click "Delete Event" 3. Confirm deletion |
| **View All** | 1. Click "Show All" to reload the complete event list |
| **Search Events** | 1. Select search type (Name/Venue/Date) 2. Enter search term 3. Click "Search" |
| **Filter by Date** | 1. Select "Filter by Date Range" 2. Enter start and end dates 3. Click "Filter" |
| **Sort Events** | 1. Select sort option (By Date/By Name) 2. Events auto-sort |
| **Export to CSV** | 1. Click "Export to CSV" 2. Choose save location 3. File saved with events |

### **Dashboard Indicators**
- **Total Events**: Shows count of all events in database
- **Upcoming Events**: Events today and in the future
- **Past Events**: Events before today

### **UI Highlights**
- Events happening within the **next 7 days** are highlighted in the table
- Click any row to auto-fill the form for editing

---

## 📊 Data Validation

The application implements **two-layer validation**:

### UI Layer (Python):
- ✓ Required fields check (Event Name, Date, Venue, Event ID)
- ✓ Date format validation (DD-MM-YYYY)
- ✓ Prevent past dates (cannot add events in the past)
- ✓ Event ID must be numeric

### Database Layer (Oracle):
- ✓ `CHECK (event_date >= TRUNC(SYSDATE))` - Prevents past dates at database level
- ✓ Primary key ensures unique Event IDs
- ✓ NOT NULL constraints on critical fields

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Python Tkinter |
| **Backend** | Python (oracledb driver) |
| **Database** | Oracle 11g |
| **OS Support** | Windows, Linux, macOS |

---

## 📝 Database Configuration (config.py)

```python
from pathlib import Path

ORACLE_CLIENT_LIB_DIR = r"C:\oracle\instantclient_19_22"  # Instant Client path
ORACLE_USER = "scott"                                      # Oracle username
ORACLE_PASSWORD = "tiger"                                  # Oracle password
ORACLE_DSN = "localhost:1521/XE"                          # Database DSN

PREVENT_PAST_DATES = True                                 # Enforce date validation
```

---

## ⚠️ Troubleshooting

### Error: "DPY-3010"
**Problem**: Oracle Instant Client not configured for thick mode
**Solution**: 
1. Download Oracle Instant Client (64-bit)
2. Set `ORACLE_CLIENT_LIB_DIR` in `config.py`
3. Restart the application

### Error: "Connection refused" or "ORA-12514"
**Problem**: Cannot connect to Oracle database
**Solution**:
1. Verify Oracle is running: `lsnrctl status` (command line)
2. Check DSN is correct (e.g., `localhost:1521/XE`)
3. Verify username and password
4. Ensure Oracle listener is active

### Error: "Table or view does not exist"
**Problem**: EVENTS table not created
**Solution**: Run `sql_queries.sql` in SQL*Plus or SQL Developer

### Upcoming Events Not Highlighted
**Problem**: Highlighting feature not working
**Solution**: Check that events have dates within the next 7 days (system date must be earlier than event date)

---

## 📚 Key Concepts Explained

### **Date Validation with TRUNC()**
- `TRUNC(SYSDATE)` returns today's date without time
- Used to compare dates ignoring time component
- Prevents past event entry at both UI and database level

### **Index Performance**
Three indexes optimize common queries:
- **idx_events_date**: Fast date range filtering
- **idx_events_name**: Fast name searches
- **idx_events_venue**: Fast venue searches

### **Case-Insensitive Search**
- Uses `UPPER()` function in SQL
- Query: `WHERE UPPER(event_name) LIKE UPPER(:1)`
- Allows matching "Event" or "EVENT" or "event"

### **Dynamic Sorting**
- `fetch_sorted_events()` accepts ORDER BY clause
- Example: `"event_date ASC"` or `"event_name DESC"`
- Flexible sorting without multiple queries

---

## 🎓 For Presentation to Teacher

### Key Points to Explain:

1. **Architecture**: Three-layer design (UI, Business Logic, Database)
2. **Database**: Oracle 11g with 4 columns + constraints + 3 indexes
3. **SQL Operations**: 14+ SQL queries for CRUD, search, filter, and statistics
4. **Validation**: Two-layer validation (UI + Database)
5. **User Features**: CRUD, search, filter, sorting, export, dashboard
6. **Code Organization**: Separation of concerns (repository pattern)
7. **Error Handling**: Connection errors, validation errors, data errors
8. **Performance**: Indexed columns for fast searches

### Files to Reference:
- `sql_queries.sql` - Show all SQL code
- `event_repository.py` - Show how queries are executed
- `college_event_management.py` - Show UI flow and validation
- `schema.sql` - Show table structure

---

## 📞 Support

For issues or questions, review:
1. `sql_queries.sql` - Understand all database operations
2. `event_repository.py` - See how queries are used
3. Troubleshooting section above

---

**Last Updated**: April 2026
**Version**: 1.0
**Database**: Oracle 11g
