-- COLLEGE EVENT MANAGEMENT SYSTEM - SQL QUERIES
-- Only the queries used in our project

-- ============================================================================
-- CREATE TABLE - Initial setup (run only once)
-- ============================================================================

CREATE TABLE events (
    event_id     NUMBER PRIMARY KEY,      -- Unique ID for each event
    event_name   VARCHAR2(120) NOT NULL, -- Name of the event
    event_date   DATE NOT NULL,          -- When the event happens
    venue        VARCHAR2(120) NOT NULL  -- Where the event happens
);

-- ============================================================================
-- 1. INSERT - Add a new event
-- Used by: add_event() function
-- ============================================================================

INSERT INTO events (event_id, event_name, event_date, venue)
VALUES (:1, :2, :3, :4);

-- EXAMPLE:
-- INSERT INTO events (event_id, event_name, event_date, venue)
-- VALUES (1, 'Tech Conference', '22-APR-2026', 'Main Hall');

-- ============================================================================
-- 2. UPDATE - Change event details
-- Used by: update_event() function
-- ============================================================================

UPDATE events
SET event_name = :1,
    event_date = :2,
    venue = :3
WHERE event_id = :4;

-- EXAMPLE:
-- UPDATE events
-- SET event_name = 'Advanced Conference', event_date = '25-APR-2026', venue = 'Hall 2'
-- WHERE event_id = 1;

-- ============================================================================
-- 3. DELETE - Remove an event
-- Used by: delete_event() function
-- ============================================================================

DELETE FROM events 
WHERE event_id = :1;

-- EXAMPLE:
-- DELETE FROM events WHERE event_id = 1;

-- ============================================================================
-- 4. SELECT ALL - Show all events sorted by date
-- Used by: fetch_all_events() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY event_date, event_id;

-- This shows all events in order of when they happen

-- ============================================================================
-- 5. SELECT WITH CUSTOM SORT - Show events sorted by any column
-- Used by: fetch_sorted_events() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY {order_clause};

-- Examples of order_clause:
-- 'event_date ASC' - earliest first
-- 'event_date DESC' - latest first
-- 'event_name ASC' - alphabetical order

-- ============================================================================
-- 6. SEARCH BY NAME - Find events by event name
-- Used by: search_by_name() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(event_name) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- EXAMPLE:
-- Search for 'con' finds: 'Conference', 'Seminar', 'Concourse' (partial match)
-- WHERE UPPER(event_name) LIKE UPPER('%con%')

-- ============================================================================
-- 7. SEARCH BY VENUE - Find events by location
-- Used by: search_by_venue() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(venue) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- EXAMPLE:
-- Search for 'Hall' finds all events in halls
-- WHERE UPPER(venue) LIKE UPPER('%Hall%')

-- ============================================================================
-- 8. SEARCH BY DATE - Find events on a specific date
-- Used by: search_by_date() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) = TRUNC(:1)
ORDER BY event_date, event_id;

-- TRUNC removes the time part, so we compare only the date
-- EXAMPLE: Find all events on 22-APR-2026

-- ============================================================================
-- 9. SEARCH BY DATE RANGE - Find events between two dates
-- Used by: filter_by_date_range() function
-- ============================================================================

SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) BETWEEN TRUNC(:1) AND TRUNC(:2)
ORDER BY event_date, event_id;

-- BETWEEN includes both start and end dates
-- EXAMPLE: Find events between 01-APR-2026 and 30-APR-2026

-- ============================================================================
-- 10. COUNT TOTAL EVENTS - How many events exist?
-- Used by: get_dashboard_counts() function
-- ============================================================================

SELECT COUNT(*) FROM events;

-- COUNT(*) counts how many rows in the table

-- ============================================================================
-- 11. COUNT UPCOMING EVENTS - How many events from today onwards?
-- Used by: get_dashboard_counts() function
-- ============================================================================

SELECT COUNT(*) FROM events 
WHERE TRUNC(event_date) >= TRUNC(SYSDATE);

-- >= means "greater than or equal to"
-- SYSDATE is today's date
-- Shows events today and in the future

-- ============================================================================
-- 12. COUNT PAST EVENTS - How many events before today?
-- Used by: get_dashboard_counts() function
-- ============================================================================

SELECT COUNT(*) FROM events 
WHERE TRUNC(event_date) < TRUNC(SYSDATE);

-- < means "less than"
-- Shows events that already happened

-- ============================================================================
