import psycopg2
from datetime import date
import hashlib


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="tbp_nvugrinec22",
        user="postgres",
        password="123"
    )

def get_plants(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT plant_id, name, image_path
        FROM plant
        WHERE user_id = %s
        ORDER BY name;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def add_plant(user_id, name, species, planting_date, image_path):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO plant (user_id, name, species, planting_date, image_path)
        VALUES (%s, %s, %s, %s, %s);
    """, (user_id, name, species, planting_date, image_path))

    conn.commit()
    cur.close()
    conn.close()


def update_plant(plant_id, name, species):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE plant
        SET name = %s,
            species = %s
        WHERE plant_id = %s;
    """, (name, species, plant_id))

    conn.commit()
    cur.close()
    conn.close()


def delete_plant(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM plant
        WHERE plant_id = %s;
    """, (plant_id,))

    conn.commit()
    cur.close()
    conn.close()


def get_plant_info(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, species, planting_date, image_path
        FROM plant
        WHERE plant_id = %s;
    """, (plant_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {
            "name": "Nepoznato",
            "species": "Nepoznato",
            "planting_date": "-",
            "image_path": None
        }

    name, species, planting_date, image_path = row
    return {
        "name": name,
        "species": species,
        "planting_date": planting_date,
        "image_path": image_path
    }



def add_event(plant_id, event_type, note):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO plant_event (plant_id, event_type, event_date, note)
        VALUES (%s, %s, %s, %s);
    """, (plant_id, event_type, date.today(), note))

    conn.commit()
    cur.close()
    conn.close()


def get_events_for_plant(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_date, event_type, note
        FROM plant_event
        WHERE plant_id = %s
        ORDER BY event_date DESC;
    """, (plant_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data



def add_growth_measurement(plant_id, height_cm):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO growth_measurement (plant_id, height_cm, measurement_date)
            VALUES (%s, %s, %s);
        """, (plant_id, height_cm, date.today()))

        conn.commit()
        return None

    except psycopg2.Error as e:
        conn.rollback()
        return str(e).split("\n")[0]

    finally:
        cur.close()
        conn.close()



def get_growth_for_plant(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT measurement_date, height_cm
        FROM growth_measurement
        WHERE plant_id = %s
        ORDER BY measurement_date DESC;
    """, (plant_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_growth_stats(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT start_height, current_height, total_growth
        FROM plant_growth_stats
        WHERE plant_id = %s;
    """, (plant_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row



def get_all_reminders(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.reminder_id,
               p.name,
               r.reminder_date,
               r.message,
               r.done,
               r.plant_id
        FROM reminder r
        JOIN plant p ON r.plant_id = p.plant_id
        WHERE p.user_id = %s
        ORDER BY r.reminder_date;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_reminders_for_plant(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT reminder_id, reminder_date, message, done
        FROM reminder
        WHERE plant_id = %s
        ORDER BY reminder_date;
    """, (plant_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def toggle_reminder_done(reminder_id):
    """
    Oznaka podsjetnika kao odrađenog.
    Sva poslovna logika (zabrane, događaji) je u triggerima u bazi.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE reminder
            SET done = NOT done
            WHERE reminder_id = %s;
        """, (reminder_id,))

        conn.commit()
        return None

    except psycopg2.Error as e:
        conn.rollback()
        return str(e).split("\n")[0]

    finally:
        cur.close()
        conn.close()


def add_reminder_rule(plant_id, title, interval_days, start_date):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO reminder_rule (plant_id, title, interval_days, start_date)
            VALUES (%s, %s, %s, %s)
            RETURNING rule_id;
        """, (plant_id, title, interval_days, start_date))

        rule_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO reminder (plant_id, reminder_date, message, rule_id)
            VALUES (%s, %s, %s, %s);
        """, (plant_id, start_date, title, rule_id))

        conn.commit()
        return None   

    except psycopg2.Error as e:
        conn.rollback()
        return str(e).split("\n")[0] 

    finally:
        cur.close()
        conn.close()



def add_plant_image(plant_id, image_path):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO plant_image (plant_id, image_path)
        VALUES (%s, %s);
    """, (plant_id, image_path))

    conn.commit()
    cur.close()
    conn.close()


def get_profile_image(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT image_path
        FROM plant_image
        WHERE plant_id = %s
          AND CURRENT_DATE <@ valid_range;
    """, (plant_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None


def get_image_gallery(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT image_path, valid_range
        FROM plant_image
        WHERE plant_id = %s
        ORDER BY lower(valid_range);
    """, (plant_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        cur.execute("""
            INSERT INTO appuser (username, password_hash)
            VALUES (%s, %s)
            RETURNING user_id;
        """, (username, password_hash))

        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return None

    finally:
        cur.close()
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("""
        SELECT user_id
        FROM appuser
        WHERE username = %s AND password_hash = %s;
    """, (username, password_hash))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def get_weekly_growth(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT week_number, weekly_growth
        FROM weekly_growth
        WHERE plant_id = %s
        ORDER BY week_number;
    """, (plant_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_fastest_growth_week(plant_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT week_number, weekly_growth
        FROM fastest_growth_week
        WHERE plant_id = %s;
    """, (plant_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

