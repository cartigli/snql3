import os
import time
import datetime
import pandas as pd
import mysql.connector
from config import *


def collector(LOCAL_DIR):
	guts_togo = []
	name_togo = []
	lo_togo = []

	for root, dirs, files in os.walk(LOCAL_DIR):
		for filename in files:
			try:
				fll_fpath = os.path.join(root, filename)
				rel_fpath = os.path.relpath(fll_fpath, LOCAL_DIR)

				ftype_ign = ('.DS_Store', '.obsidian', '.git')
				if any(term in fll_fpath for term in ftype_ign):
					print(f"{filename}\'s spoofed.")

				else:
					with open (fll_fpath, 'r', encoding='utf-8') as f:
						guts = f.read()
						guts_togo.append(guts)
						
					lo_togo.append(rel_fpath)
					name_togo.append(filename)

			except UnicodeDecodeError:
				print(f"ENCODING ERR ON {filename}.")
				continue
			except PermissionError:
				print(f"PERMISSION ERR ON {filename}.")
				continue
			except Exception as e:
				print(f"ERR: {e} ON {filename}.")
				continue

	return guts_togo, name_togo, lo_togo


def container(guts_togo, name_togo, lo_togo):
	guts_glory = pd.DataFrame({
		'note_tl': name_togo,
		'note_lo': lo_togo,
		'note': guts_togo
		})
		
	ensemble = guts_glory.to_records()

	return ensemble


def initialize_connection(USER, PSWD, NAME, ADDR):
	try:
		conn = mysql.connector.connect(
			host=ADDR,
			user=USER,
			password=PSWD,
			database=NAME
		)

		return conn
		
	except Exception as e:
		print(f"ERR: {e}; CHECK CONFIG!")

		return None


def table_support(conn):
	cursor = conn.cursor()

	ut_c = datetime.datetime.now(datetime.UTC)
	time_0 = ut_c.strftime('%Y%m%d%H%M%S%z')
	time = time_0.replace('+', 'plus').replace('-', 'less')

	title = f"de"
	t_name = (f"{title}_{time}")

	q = f"CREATE TABLE IF NOT EXISTS {t_name} (note_no INT NOT NULL AUTO_INCREMENT, note_tl VARCHAR(75) NOT NULL, note_lo VARCHAR(255) NOT NULL, note TEXT CHARACTER SET utf8mb4, PRIMARY KEY (note_no));"
	cursor.execute(q)

	return t_name


def upload(conn, t_name, contained):
	cursor = conn.cursor()
	
	q = f"INSERT INTO {t_name} (note_tl, note_lo, note) VALUES (%s, %s, %s);"
	cursor.executemany(q, contained)
	
	conn.commit()


if __name__=="__main__":
	collected = collector(LOCAL_DIR)
	contained = container(*collected)
	
	conn = initialize_connection(USER, PSWD, NAME, ADDR)
	t_name = table_support(conn)

	data = [(row.note_tl, row.note_lo, row.note) for row in contained]
	upload(conn, t_name, data)
	
	conn.close()
