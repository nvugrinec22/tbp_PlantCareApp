CREATE TABLE appuser (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE plant (
    plant_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100),
    planting_date DATE,
    image_path TEXT,

    CONSTRAINT fk_plant_user
        FOREIGN KEY (user_id)
        REFERENCES appuser(user_id)
        ON DELETE CASCADE
);


CREATE TABLE plant_event (
    event_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL,
    event_type event_type_enum NOT NULL,
    event_date DATE NOT NULL,
    note TEXT,

    CONSTRAINT fk_event_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
        ON DELETE CASCADE
);


CREATE TABLE growth_measurement (
    measurement_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL,
    height_cm positive_height NOT NULL,
    measurement_date DATE NOT NULL,

    CONSTRAINT fk_measurement_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
        ON DELETE CASCADE
);


CREATE TABLE reminder_rule (
    rule_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    interval_days INTEGER NOT NULL CHECK (interval_days > 0),
    start_date DATE NOT NULL,
    active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_rule_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
        ON DELETE CASCADE
);


CREATE TABLE reminder (
    reminder_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL,
    rule_id INTEGER,
    reminder_date DATE NOT NULL,
    message TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_reminder_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reminder_rule
        FOREIGN KEY (rule_id)
        REFERENCES reminder_rule(rule_id)
        ON DELETE CASCADE
);


CREATE TABLE plant_image (
    image_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    valid_range DATERANGE NOT NULL,

    CONSTRAINT fk_image_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
        ON DELETE CASCADE
);

