
```python
import os
import pandas as pd
import mysql.connector
#from config import * # import env variables from env file

# in place of future env file
USER = 'py'
PASS_PHRASE = '0n3*4t!2D*62'
DATABASE_NAME = 'employees'
TABLE_NAME = 'notes'
DATABASE_ADDR = '192.168.1.68'
HOST_PORT = 3306
#ALLOWED_PACKETS = 67108864
#LOCAL_DIR = '/home/tom/vault'\
LOCAL_DIR = '/Volumes/HomeXx/compuir/vault'

def initialize_connection(DATABASE_ADDR, HOST_PORT, USER, PASS_PHRASE, DATABASE_NAME):
	try:
		conn = mysql.connector.connect(
			host=DATABASE_ADDR,
			user=USER,
			password=PASS_PHRASE,
			database=DATABASE_NAME
		)
		return conn
	except Exception as e:
		print(f"ERR {e}: CHECK DB_CONFIG")
		return None


def table_support(conn, TABLE_NAME):
	cursor = conn.cursor()	
	cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (note_no INT NOT NULL AUTO_INCREMENT,\nnote_tl VARCHAR(75) NOT NULL,\nnote_lo VARCHAR(255) NOT NULL,\nnote_ TEXT CHARACTER SET utf8mb4,\nPRIMARY KEY (note_no)\n);") # used a string but will change after testing



def upload(conn, TABLE_NAME):
	cursor = conn.cursor()

	cursor.execute(f"INSERT INTO {TABLE_NAME} (note_tl, note_lo, note_) VALUES ('new_note', '/Volumes/vault/new_note', 'blah blah blah');")
	conn.commit()
	cursor.close()


conn = initialize_connection(DATABASE_ADDR, HOST_PORT, USER, PASS_PHRASE, DATABASE_NAME)
table_support(conn, TABLE_NAME)
upload(conn, TABLE_NAME)
```
Bada-bing, bada-boom.