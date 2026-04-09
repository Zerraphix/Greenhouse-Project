from time import sleep
import sqlite3
from datetime import datetime
from ADC_MCP3021 import MCP3021


def create_table():
    query = """CREATE TABLE IF NOT EXISTS soil (
                datetime TEXT NOT NULL,
                raw REAL NOT NULL,
                percent REAL NOT NULL
            )"""
    conn = None
    try:
        conn = sqlite3.connect('database/sensor_data.db')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"Error connecting to database: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

def log_soil_MCP3021():
    while True:
        query = """INSERT INTO soil (datetime, raw, percent) VALUES (?, ?, ?)"""
        sensor = MCP3021()
        now = datetime.now()
        now = now.strftime("%d/%m/%y - %H:%M:%S")
        data = (now, sensor.read_raw(), sensor.read_percent())
        conn = None
        try:
            conn = sqlite3.connect('database/sensor_data.db')
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

        except sqlite3.Error as sql_e:
            print(f"Error connecting to database: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()
        sleep(2)
                
create_table()
log_soil_MCP3021()