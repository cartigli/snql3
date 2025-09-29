import os
import pandas as pd
import mysql.connector
from config import *

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
				ftype_ign = ('.DS_Store', '.obsidian', '.git')
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

	return guts_togo, name_togo, lo_togo

def container(guts_togo, name_togo, lo_togo):
	guts_glory = pd.DataFrame({
		'note_tl': name_togo,
		'note_lo': lo_togo,
		'note': guts_togo
		})
	ensemble = guts_glory.to_records()
	return ensemble

def initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, DATABASE_ADDR):
	try:
		conn = mysql.connector.connect(
			host=DATABASE_ADDR,
			user=DB_USER,
			password=PASS_PHRASE,
			database=DATABASE_NAME
		)
		return conn
	except Exception as e:
		print(f"ERR {e}: CHECK CONFIG")
		return None

def table_support(conn, TABLE_NAME):
	cursor = conn.cursor()	
	cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (note_no INT NOT NULL AUTO_INCREMENT, note_tl VARCHAR(75) NOT NULL, note_lo VARCHAR(255) NOT NULL, note TEXT CHARACTER SET utf8mb4, PRIMARY KEY (note_no));")

def upload(conn, TABLE_NAME, contained):
	cursor = conn.cursor()
	query = f"INSERT INTO {TABLE_NAME} (note_tl, note_lo, note) VALUES (%s, %s, %s);"
	cursor.executemany(query, contained)
	conn.commit()
	conn.close()

if __name__=="__main__":
	collected = collector(LOCAL_DIR)
	contained = container(*collected)
	
	conn = initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, DATABASE_ADDR)
	table_s = table_support(conn, TABLE_NAME)	

	data = [(row.note_tl, row.note_lo, row.note) for row in contained]
	upload(conn, TABLE_NAME, data)


