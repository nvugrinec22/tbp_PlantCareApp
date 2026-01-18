
CREATE OR REPLACE RULE ignore_duplicate_reminder AS
ON INSERT TO reminder
WHERE EXISTS (
    SELECT 1
    FROM reminder r
    WHERE r.plant_id = NEW.plant_id
      AND r.reminder_date = NEW.reminder_date
      AND r.message = NEW.message
)
DO INSTEAD NOTHING;
