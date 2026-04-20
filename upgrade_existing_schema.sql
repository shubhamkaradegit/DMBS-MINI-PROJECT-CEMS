-- Upgrade script for existing installations
-- Use this if EVENTS table already exists and has data.
-- 1) Add date check constraint if missing
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

-- 2) Create venue index if missing
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM user_indexes WHERE index_name = 'IDX_EVENTS_VENUE';
    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE INDEX idx_events_venue ON events(venue)';
    END IF;
END;
/
