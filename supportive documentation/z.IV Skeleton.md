```python
import os
import pandas as pd
import mysql.connector
#from config import * # import env variables from env file

# in place of future env file
USER = 'thinker'
PASS_PHRASE = 'password'
DATABASE_NAME = 'cave'
TABLE_NAME = 'notes_'
DATABASE_ADDR = '192.168.1.68'
HOST_PORT = 3306
ALLOWED_PACKETS = 67108864
LOCAL_DIR = '/home/tom/vault'


def collector(LOCAL_DIR):
	folder_path = LOCAL_DIR
	guts_togo = []
	name_togo = []
	lo_togo = []
	spoofed = []
	add_err = []
	for root, dirs, files in os.walk(folder_path):
		for filename in files:
			try:
				fll_fpath = os.path.join(root, filename)
				ftype_ign = (".DS_Store", ".obsidian", ".git")
				if any(term in fll_fpath for term in ftype_ign):
					spoofed.append(filename)
					print(f"{filename}\'s spoofed.")
				else:
					with open (fll_fpath, 'r', encoding='utf-8') as f:
						guts = f.read()
						guts_togo.append(guts)

					lo_togo.append(fll_fpath)
					name_togo.append(filename)
			except UnicodeDecodeError:
				print(f"ENCODING ERR: {filename}.")
				add_err.append(filename)
				continue
			except FileNotFoundError:
				print(f"FILE NOT FOUND: {filename}.")
				add_err.append(filename)
			except PermissionError:
				print(f"PERMISSION ERR: {filename}.")
				add_err.append(filename)
			except Exception as e:
				print(f"ERR {e}: {filename}.")
				add_err.append(filename)

	return guts_togo, name_togo, lo_togo, add_err


def container(guts_togo, name_togo, lo_togo):
	guts_glory = pd.DataFrame({
		'note_tl': name_togo,
		'note_lo': lo_togo,
		'note': guts_togo
		})
	guts = guts_glory.to_records()
	return ensemble


def initialize_connection(USER, PASS_PHRASE, DATABASE_NAME, TABLE_NAME, DATABASE_ADDR, HOST_PORT, ALLOWED_PACKETS):
	conn = mysql.connector.connect(
		host=DATABASE_ADDR,
		port=HOST_PORT,
		user=USER,
		password=PASS_PHRASE,
		database=DATABASE_NAME,
		max_allowed_packet=ALLOWED_PACKETS
		)
	return conn


def check_ftable(conn, TABLE_NAME):
	cursor = conn.cursor()
	cursor.execute(f"SELECT * FROM {TABLE_NAME}")
	results = cursor.fetchall()
	cursor.close()
	return results


def table_support(conn, TABLE_NAME):
	cursor = conn.cursor()	
	cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (note_no INT NOT NULL AUTO_INCREMENT,\nnote_tl VARCHAR(75) NOT NULL,\nnote_lo VARCHAR(255) NOT NULL,\nnote_ TEXT CHARACTER SET utf8mb64,\nPRIMARY KEY (note_no)\n);") # used a string but will change after testing
	cursor.close()


def upload(conn, TABLE_NAME, ensemble):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO",TABLE_NAME,"(note_no, note_tl, note_lo, note_) VALUES (%s, %s, %s, %s);"),
		guts_glory # need index from df as well
	)
	cursor.commit()
	cursor.close()


def hindsight(conn, TABLE_NAME):
	cursor = conn.cursor()
	cursor.execute(f"SELECT * FROM {TABLE_NAME}")
	hs = cursor.fetchmany(5)
	print(f"When checking table for new data, we found:{hs}")
	cursor.close()


def main(USER, PASS_PHRASE, DATABASE_NAME, TABLE_NAME, DATABASE_ADDR, HOST_PORT, ALLOWED_PACKETS, LOCAL_DIR):
	conn = initialize_connection(USER, PASS_PHRASE, DATABASE_NAME, TABLE_NAME, DATABASE_ADDR, HOST_PORT, ALLOWED_PACKETS)
	
	collected = collector(LOCAL_DIR)
	guts = container(*collected) # unpack the collected, contain

	table_support(conn, TABLE_NAME)
	upload(conn, TABLE_NAME, guts)
```

Config.py
```python
import os

USER = os.getenv('USER','thinker')
PASS_PHRASE = os.getenv('PASS_PHRASE','password')
DATABASE_NAME = os.getenv('DATABASE_NAME','cave')
TABLE_NAME = os.getenv('TABLE_NAME','notes_')
DATABASE_ADDR = os.getenv('DATABASE_ADDR','192.168.1.68')
HOST_PORT = os.getenv('HOST_PORT','3306')
ALLOWED_PACKETS = os.getenv('ALLOWED_PACKETS',67108864)

LOCAL_DIR = os.getenv('LOCAL_DIR','/file/path')
```