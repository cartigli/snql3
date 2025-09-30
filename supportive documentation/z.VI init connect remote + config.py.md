```python
import os
import pandas as pd
import mysql.connector
from config import * # import env variables from env file


def initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, TABLE_NAME, DATABASE_ADDR, HOST_PORT):
	conn = mysql.connector.connect(
		host=DATABASE_ADDR,
		port=HOST_PORT,
		user=DB_USER,
		password=PASS_PHRASE,
		database=DATABASE_NAME,
		#max_allowed_packet=ALLOWED_PACKETS
		)
	return conn

conn = initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, TABLE_NAME, DATABASE_ADDR, HOST_PORT)
cursor = conn.cursor()

cursor.execute(f"SELECT * FROM notes;")
print(cursor.fetchall())
```

Obvious in hindsight, but User needs A. a strong password and B. permission to access the given database. 

```python
import os

DB_USER = os.getenv('DB_USER','py')
PASS_PHRASE = os.getenv('PASS_PHRASE','0n3*4t!2D*62')
DATABASE_NAME = os.getenv('DATABASE_NAME','employees')
TABLE_NAME = os.getenv('TABLE_NAME','employees')
DATABASE_ADDR = os.getenv('DATABASE_ADDR','192.168.1.68')
HOST_PORT = os.getenv('HOST_PORT','3306')
ALLOWED_PACKETS = os.getenv('ALLOWED_PACKETS',67108864)

LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/vault')
```