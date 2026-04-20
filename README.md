College Event Management System (Tkinter + Oracle 11g)

Files
- college_event_management.py : Main app controller and business flow
- ui_layout.py : Tkinter layout and widget construction
- event_repository.py : Oracle database operations and query layer
- config.py : Database credentials and app configuration
- schema.sql : Oracle table creation script
- upgrade_existing_schema.sql : Upgrade script for existing EVENTS table without dropping data

Setup
1. Install Python dependency:
   pip install oracledb

2. Oracle 11g requires thick mode with Oracle Instant Client:
   - Download Oracle Instant Client (64-bit) from Oracle website.
   - Extract it to a folder, for example: C:\\oracle\\instantclient_19_22
   - In college_event_management.py, set ORACLE_CLIENT_LIB_DIR to that folder path.

3. Create table in Oracle:
   - Open SQL Developer or SQL*Plus
   - Run schema.sql

   Note:
   - schema.sql adds check constraint to prevent past event dates

   If table already exists with data:
   - Run upgrade_existing_schema.sql instead of recreating table

4. Open college_event_management.py and update these constants:
   - ORACLE_USER
   - ORACLE_PASSWORD
   - ORACLE_DSN
   - ORACLE_CLIENT_LIB_DIR (required for Oracle 11g)

   Example DSN values:
   - localhost:1521/XE
   - localhost:1521/ORCL

Run
python college_event_management.py

Features
- CRUD (Add / Update / Delete / Show All)
- Manual Event ID entry
- Search by Event Name, Date, and Venue
- Filter events by date range
- Sorting by Date and Name
- Dashboard counters:
   - Total events
   - Upcoming events
   - Past events
- Upcoming events (next 7 days) highlighted in table
- Click any row to auto-fill form for editing
- Export current table rows to CSV
- Input validation:
   - Required fields
   - Date format DD-MM-YYYY
   - Prevent past dates (UI + DB check constraint)
