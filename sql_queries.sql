-- COLLEGE EVENT MANAGEMENT SYSTEM - SQL QUERIES
-- Simple version for beginners

-- ============================================================================
-- TABLE CREATION (Run this once to create the table)
-- ============================================================================

CREATE TABLE events (
    event_id     NUMBER PRIMARY KEY,           -- Unique ID for each event
    event_name   VARCHAR2(120) NOT NULL,      -- Name of the event
    event_date   DATE NOT NULL,               -- When the event happens
    venue        VARCHAR2(120) NOT NULL,      -- Where the event happens
    created_at   DATE DEFAULT SYSDATE NOT NULL -- When record was created
);

-- ============================================================================
-- CREATE INDEXES (Makes searching faster)
-- ============================================================================

CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_name ON events(event_name);
CREATE INDEX idx_events_venue ON events(venue);

-- ============================================================================
-- INSERT - Add a new event
-- ============================================================================
-- :1 = event_id, :2 = event_name, :3 = event_date, :4 = venue

INSERT INTO events (event_id, event_name, event_date, venue)
VALUES (:1, :2, :3, :4);

-- ============================================================================
-- UPDATE - Change an existing event
-- ============================================================================
-- :1 = new event_name, :2 = new event_date, :3 = new venue, :4 = event_id

UPDATE events
SET event_name = :1,
    event_date = :2,
    venue = :3
WHERE event_id = :4;

-- ============================================================================
-- DELETE - Remove an event
-- ============================================================================
-- :1 = event_id (the ID of event to delete)

DELETE FROM events 
WHERE event_id = :1;

-- ============================================================================
-- SEARCH QUERIES - Find events in different ways
-- ============================================================================

-- SEARCH 1 - Find all events (sorted by date)
-- Shows all events ordered by when they happen

SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY event_date, event_id;

-- ============================================================================

-- SEARCH 2 - Sort events in different ways
-- :1 = how you want to sort (example: "event_date ASC" or "event_name DESC")
-- ASC = smallest to biggest, DESC = biggest to smallest

SELECT event_id, event_name, event_date, venue
FROM events
ORDER BY {order_clause};

-- ============================================================================

-- SEARCH 3 - Find events by name (search for part of the name)
-- :1 = text to search (example: if you type "con%", it finds "Conference")
-- UPPER() ignores uppercase/lowercase differences
-- LIKE means 'contains or matches'

SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(event_name) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- SEARCH 4 - Find events by venue (search for part of the venue)
-- :1 = venue name to search (example: "Hall%" finds all halls)

SELECT event_id, event_name, event_date, venue
FROM events
WHERE UPPER(venue) LIKE UPPER(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- SEARCH 5 - Find events on exactly one date
-- :1 = the date you want to find
-- TRUNC() removes the time, keeps only the date part
-- = means exactly equal to this date

SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) = TRUNC(:1)
ORDER BY event_date, event_id;

-- ============================================================================

-- SEARCH 6 - Find events between two dates (date range)
-- :1 = start date, :2 = end date
-- BETWEEN finds events on or after start date AND on or before end date

SELECT event_id, event_name, event_date, venue
FROM events
WHERE TRUNC(event_date) BETWEEN TRUNC(:1) AND TRUNC(:2)
ORDER BY event_date, event_id;

-- ============================================================================
-- STATISTICS - Get counts and summaries
-- ============================================================================

-- STAT 1 - Count total events in database
-- COUNT(*) counts how many rows exist

SELECT COUNT(*) FROM events;

-- ============================================================================

-- STAT 2 - Count upcoming events (today and future)
-- >= means greater than or equal to
-- SYSDATE is today's date

SELECT COUNT(*) FROM events 
WHERE TRUNC(event_date) >= TRUNC(SYSDATE);

-- ============================================================================

-- STAT 3 - Count past events (before today)
-- < means less than

SELECT COUNT(*) FROM events 
WHERE TRUNC(event_date) < TRUNC(SYSDATE);
