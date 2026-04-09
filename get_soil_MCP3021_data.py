from time import sleep
import sqlite3
from datetime import datetime

def get_soil_data(number_of_rows):    
        query = """SELECT * FROM soil ORDER BY datetime DESC"""
        datetimes = []
        raw = []
        percent = []
        conn = None
        try:
            conn = sqlite3.connect('database/sensor_data.db')
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[0])
                raw.append(row[1])
                percent.append(row[2])
            return datetimes, raw, percent
        except sqlite3.Error as sql_e:
            print(f"Error connecting to database: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()

                

# get_soil_data(10)