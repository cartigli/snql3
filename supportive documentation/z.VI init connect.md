```python
import os
import pandas as pd
import mysql.connector
#from config import * # import env variables from env file

# in place of future env file
USER = 'root'
PASS_PHRASE = 'koipo222'
DATABASE_NAME = 'emp'
TABLE_NAME = 'employees'
DATABASE_ADDR = '127.0.0.1'
HOST_PORT = 3306
#ALLOWED_PACKETS = 67108864
#LOCAL_DIR = '/home/tom/vault'\
LOCAL_DIR = '/Volumes/HomeXx/compuir/vault'

def initialize_connection(DATABASE_ADDR, HOST_PORT, USER, PASS_PHRASE, DATABASE_NAME):
    try:
        conn = mysql.connector.connect(
		    host=DATABASE_ADDR,
		    #port=HOST_PORT,
		    user=USER,
		    password=PASS_PHRASE,
		    database=DATABASE_NAME
		    #max_allowed_packet=ALLOWED_PACKETS
		)
		return conn
    except Exception as e:
        print(f"ERR {e}: CHECK DB_CONFIG")
        return None

conn = initialize_connection(DATABASE_ADDR, HOST_PORT, USER, PASS_PHRASE, DATABASE_NAME)
cursor = conn.cursor()

cursor.execute(f"SELECT * FROM employees;")
con = cursor.fetchall()

print(con)

```