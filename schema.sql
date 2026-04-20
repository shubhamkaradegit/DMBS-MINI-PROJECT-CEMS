-- College Event Management System table (Oracle 11g)
-- Run this script once in SQL*Plus / SQL Developer

CREATE TABLE events (
    event_id     NUMBER PRIMARY KEY,
    event_name   VARCHAR2(120) NOT NULL,
    event_date   DATE NOT NULL,
    venue        VARCHAR2(120) NOT NULL,
    created_at   DATE DEFAULT SYSDATE NOT NULL
);

CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_name ON events(event_name);
