College Event Management System (Tkinter + Oracle 11g)

Files
- college_event_management.py : Main Tkinter application with CRUD operations
- schema.sql : Oracle table creation script

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
- Add Event
- Update Event
- Delete Event
- View All Events
- Click any row to auto-fill the form
- Input validation:
  - Event ID must be numeric
  - Date format must be DD-MM-YYYY
