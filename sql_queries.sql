-- ============================================================================
-- COLLEGE EVENT MANAGEMENT SYSTEM - COMPLETE SQL QUERIES
-- ============================================================================
-- Database: Oracle 11g
-- This file contains ALL SQL code used in the project.
-- Run these scripts in SQL*Plus or SQL Developer.
-- ============================================================================

-- SECTION 1: TABLE CREATION (Run once during initial setup)
-- ============================================================================

CREATE TABLE events (
    event_id     NUMBER PRIMARY KEY,
    event_name   VARCHAR2(120) NOT NULL,
    event_date   DATE NOT NULL,
    venue        VARCHAR2(120) NOT NULL,
    created_at   DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT chk_event_date CHECK (event_date >= TRUNC(SYSDATE))
);

-- ============================================================================
-- SECTION 2: INDEX CREATION (Improves query performance)
-- ============================================================================

CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_name ON events(event_name);
CREATE INDEX idx_events_venue ON events(venue);

-- ============================================================================
-- SECTION 3: UPGRADE SCRIPT FOR EXISTING INSTALLATIONS
-- ============================================================================
-- Use this if EVENTS table already exists and has data.
-- These scripts safely add constraints and indexes without data loss.

-- 3.1: Add date check constraint if missing
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM user_constraints
    WHERE constraint_name = 'CHK_EVENT_DATE'
      AND table_name = 'EVENTS';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE events ADD CONSTRAINT chk_event_date CHECK (event_date >= TRUNC(SYSDATE))';
    END IF;
END;
/

-- 3.2: Create venue index if missing
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM user_indexes WHERE index_name = 'IDX_EVENTS_VENUE';
    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE INDEX idx_events_venue ON events(venue)';
    END IF;
END;
/

-- ============================================================================
-- SECTION 4: CRUD OPERATIONS (Used by the application)
-- ============================================================================

-- 4.1: INSERT - Add a new event
-- Called by: EventRepository.add_event()
-- Parameters: event_id, event_name, event_date, venue
INSERT INTO events (event_id, event_name, event_date, venue)
VALUES (:1, :2, :3, :4);

-- ============================================================================

-- 4.2: UPDATE - Modify an existing event
-- Called by: EventRepository.update_event()
-- Parameters: event_name, event_date, venue, event_id
UPDATE events
SET event_name = :1,
    event_date = :2,
    venue = :3
WHERE event_id = :4;

-- ============================================================================

-- 4.3: DELETE - Remove an event
-- Called by: EventRepository.delete_event()
-- Parameters: event_id
DELETE FROM events WHERE event_id = :1;

-- ============================================================================
-- SECTION 5: READ OPERATIONS - FETCH ALL EVENTS
-- ============================================================================

-- 5.1: Fetch all events (sorted by date and ID)
-- Called by: EventRepository.fetch_all_events()
-- Returns: All events ordered by event_date ascending
SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY event_date, event_id;

-- ============================================================================

-- 5.2: Fetch sorted events (dynamic sorting)
-- Called by: EventRepository.fetch_sorted_events()
-- Parameters: order_clause (e.g., "event_date ASC", "event_name DESC")
-- Returns: Events with custom sort order
SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY {order_clause};

-- ============================================================================
-- SECTION 6: SEARCH OPERATIONS
-- ============================================================================

-- 6.1: Search events by name (case-insensitive)
-- Called by: EventRepository.search_by_name()
-- Parameters: search_text (partial match)
-- Returns: Events matching the name pattern
SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(event_name) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- 6.2: Search events by venue (case-insensitive)
-- Called by: EventRepository.search_by_venue()
-- Parameters: search_text (partial match)
-- Returns: Events matching the venue pattern
SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(venue) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- 6.3: Search events by exact date
-- Called by: EventRepository.search_by_date()
-- Parameters: parsed_date
-- Returns: Events on the specified date
SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) = TRUNC(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- 6.4: Filter events by date range
-- Called by: EventRepository.filter_by_date_range()
-- Parameters: start_date, end_date
-- Returns: Events between the date range (inclusive)
SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) BETWEEN TRUNC(:1) AND TRUNC(:2)
ORDER BY event_date, event_id;

-- ============================================================================
-- SECTION 7: DASHBOARD STATISTICS
-- ============================================================================

-- 7.1: Count total events
-- Called by: EventRepository.get_dashboard_counts()
-- Returns: Total number of events in database
SELECT COUNT(*) FROM events;

-- ============================================================================

-- 7.2: Count upcoming events (today and future)
-- Called by: EventRepository.get_dashboard_counts()
-- Returns: Number of events with date >= today
SELECT COUNT(*) FROM events WHERE TRUNC(event_date) >= TRUNC(SYSDATE);

-- ============================================================================

-- 7.3: Count past events (before today)
-- Called by: EventRepository.get_dashboard_counts()
-- Returns: Number of events with date < today
SELECT COUNT(*) FROM events WHERE TRUNC(event_date) < TRUNC(SYSDATE);

-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================
