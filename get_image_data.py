import sqlite3


def get_images(number_of_rows):
    try:
        number_of_rows = int(number_of_rows)
    except ValueError:
        number_of_rows = 10

    if number_of_rows < 1:
        number_of_rows = 10

    query = f"""SELECT timestamp FROM images ORDER BY timestamp DESC LIMIT {number_of_rows}"""

    timestamps = []
    conn = None
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        for row in rows:
            timestamps.append(row[0])

        return timestamps

    except sqlite3.Error as sql_e:
        print(f"Error connecting to database: {sql_e}")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        if conn:
            conn.close()


def get_latest_image():
    query = """SELECT timestamp FROM images ORDER BY timestamp DESC LIMIT 1"""

    conn = None
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        row = cur.fetchone()

        if row:
            return row[0]
        return None

    except sqlite3.Error as sql_e:
        print(f"Error connecting to database: {sql_e}")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        if conn:
            conn.close()