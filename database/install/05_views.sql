
CREATE VIEW plant_growth_stats AS
SELECT
    plant_id,
    MIN(height_cm) AS start_height,
    MAX(height_cm) AS current_height,
    MAX(height_cm) - MIN(height_cm) AS total_growth
FROM growth_measurement
GROUP BY plant_id;


CREATE VIEW weekly_growth AS
SELECT
    gm.plant_id,
    (FLOOR((gm.measurement_date - p.planting_date) / 7) + 1)::INT AS week_number,
    MIN(gm.height_cm) AS start_height,
    MAX(gm.height_cm) AS end_height,
    MAX(gm.height_cm) - MIN(gm.height_cm) AS weekly_growth
FROM growth_measurement gm
JOIN plant p ON p.plant_id = gm.plant_id
GROUP BY
    gm.plant_id,
    week_number;




CREATE VIEW fastest_growth_week AS
SELECT DISTINCT ON (plant_id)
    plant_id,
    week_number,
    weekly_growth
FROM weekly_growth
ORDER BY plant_id, weekly_growth DESC;
