CREATE OR REPLACE FUNCTION set_profile_image()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE plant_image
    SET valid_range = daterange(
        lower(valid_range),
        CURRENT_DATE,
        '[)'
    )
    WHERE plant_id = NEW.plant_id
      AND valid_range IS NOT NULL
      AND CURRENT_DATE <@ valid_range;

    NEW.valid_range := daterange(CURRENT_DATE, 'infinity', '[)');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_set_profile_image
BEFORE INSERT ON plant_image
FOR EACH ROW
EXECUTE FUNCTION set_profile_image();





CREATE OR REPLACE FUNCTION create_initial_measurement_reminder()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO reminder (plant_id, reminder_date, message, done)
    VALUES (
        NEW.plant_id,
        NEW.planting_date,
        'Vrijeme je za pocetno mjerenje visine biljke',
        FALSE
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_initial_measurement_reminder
AFTER INSERT ON plant
FOR EACH ROW
EXECUTE FUNCTION create_initial_measurement_reminder();


CREATE OR REPLACE FUNCTION start_periodic_measurement()
RETURNS TRIGGER AS $$
DECLARE
    v_rule_id INTEGER;
BEGIN
    IF OLD.done = FALSE
       AND NEW.done = TRUE
       AND NEW.message = 'Vrijeme je za pocetno mjerenje visine biljke' THEN

        INSERT INTO reminder_rule (plant_id, title, interval_days, start_date)
        VALUES (
            NEW.plant_id,
            'Mjerenje visine biljke',
            5,
            CURRENT_DATE
        )
        RETURNING rule_id INTO v_rule_id;

        INSERT INTO reminder (plant_id, reminder_date, message, rule_id)
        VALUES (
            NEW.plant_id,
            CURRENT_DATE + INTERVAL '5 days',
            'Vrijeme je za mjerenje visine biljke',
            v_rule_id
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_start_measurement_cycle
AFTER UPDATE OF done ON reminder
FOR EACH ROW
EXECUTE FUNCTION start_periodic_measurement();




CREATE OR REPLACE FUNCTION prevent_early_reminder_completion()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.done = FALSE
       AND NEW.done = TRUE
       AND CURRENT_DATE < NEW.reminder_date THEN

        RAISE EXCEPTION
        'Ne možeš označiti podsjetnik kao odrađen prije datuma (%).',
        NEW.reminder_date;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_prevent_early_completion
BEFORE UPDATE OF done ON reminder
FOR EACH ROW
EXECUTE FUNCTION prevent_early_reminder_completion();



CREATE OR REPLACE FUNCTION prevent_empty_reminder_fn()
RETURNS TRIGGER AS $$
BEGIN
    IF trim(NEW.message) = '' THEN
        RAISE EXCEPTION 'Poruka podsjetnika ne smije biti prazna';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_empty_reminder
BEFORE INSERT ON reminder
FOR EACH ROW
EXECUTE FUNCTION prevent_empty_reminder_fn();



CREATE OR REPLACE FUNCTION validate_growth_measurement()
RETURNS TRIGGER AS $$
DECLARE
    last_height NUMERIC;
BEGIN
    SELECT height_cm
    INTO last_height
    FROM growth_measurement
    WHERE plant_id = NEW.plant_id
    ORDER BY measurement_date DESC
    LIMIT 1;

    IF last_height IS NOT NULL THEN
        IF NEW.height_cm < last_height THEN
            RAISE EXCEPTION
            'Nova visina (%.2f cm) ne smije biti manja od prethodne (%.2f cm)',
            NEW.height_cm, last_height;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validate_growth
BEFORE INSERT ON growth_measurement
FOR EACH ROW
EXECUTE FUNCTION validate_growth_measurement();


CREATE OR REPLACE FUNCTION create_next_periodic_reminder()
RETURNS TRIGGER AS $$
DECLARE
    v_interval INTEGER;
    v_message  TEXT;
BEGIN
    IF OLD.done = FALSE AND NEW.done = TRUE AND NEW.rule_id IS NOT NULL THEN

        SELECT interval_days, title
        INTO v_interval, v_message
        FROM reminder_rule
        WHERE rule_id = NEW.rule_id
          AND active = TRUE;

        IF v_interval IS NOT NULL THEN
            INSERT INTO reminder (
                plant_id,
                rule_id,
                reminder_date,
                message,
                done
            )
            VALUES (
                NEW.plant_id,
                NEW.rule_id,
                NEW.reminder_date + (v_interval || ' days')::INTERVAL,
                v_message,
                FALSE
            );
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_create_next_periodic_reminder
AFTER UPDATE OF done ON reminder
FOR EACH ROW
EXECUTE FUNCTION create_next_periodic_reminder();
