import sqlite3


def create_image_table():
    query = """
        CREATE TABLE IF NOT EXISTS images (
            timestamp TEXT NOT NULL
        )
    """

    conn = None
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"Error connecting to database: {sql_e}")
        if conn:
            conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


def insert_image(timestamp):
    query = """INSERT INTO images (timestamp) VALUES (?)"""

    conn = None
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, (timestamp,))
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"Error connecting to database: {sql_e}")
        if conn:
            conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()