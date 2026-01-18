
CREATE DOMAIN positive_height NUMERIC(5,2)
CHECK (VALUE > 0);



CREATE TYPE event_type_enum AS ENUM (
    'watering',
    'fertilizing',
    'measurement',
    'repotting',
    'pruning',
    'other'
);