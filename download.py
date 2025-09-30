import os
import os
import pandas as pd
import mysql.connector
from config import *


def survey_db(conn, DB_NAME):
	cursor = conn.cursor()

	q = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{DB_NAME}' ORDER BY table_name DESC;"
	cursor.execute(q)

	tables = cursor.fetchall()
	table = tables[0][0]

	return table


def survey_t(conn, table):
	cursor = conn.cursor()

	q = f"SELECT * FROM {table}"
	cursor.execute(q)
	guts = cursor.fetchall()

	return guts

 
def layout_guts(guts):
	note_name = []
	note_lo = []
	note_guts = []
	patched_path = []

	for record in guts:
		note_name.append(record[1])

		rel_path = record[2]
		new_path = os.path.join(LOCAL_DIR, rel_path)
		repaired_path = os.path.normpath(new_path) # win
		note_lo.append(repaired_path)

		note_guts.append(record[3])

	return note_name, note_lo, note_guts


def contain(note_name, note_lo, note_guts):
	notes = pd.DataFrame({
			'name': note_name,
			'path': note_lo,
			'contents': note_guts
		})

	return notes


def write_to_disk(notes):
	for index, row in notes.iterrows():
		path = row['path']
		contents = row['contents']
		directory = os.path.dirname(path)
		os.makedirs(directory, exist_ok=True)
		with open(path, 'w', encoding='utf-8') as f:
			f.write(contents)


def initialize_connection(DB_USER, DB_PASS, DB_NAME, DB_ADDR):
	try:
		conn = mysql.connector.connect(
			host=DB_ADDR,
			user=DB_USER,
			password=DB_PASS,
			database=DB_NAME
		)

		return conn
	except Exception as e:
		print(f"ERR {e}: CHECK CONFIG")

		return None


if __name__ == "__main__":
	conn = initialize_connection(DB_USER, DB_PASS, DB_NAME, DB_ADDR)
	if conn:
		try:
			tables = survey_db(conn, DB_NAME)
			table = survey_t(conn, tables)
			guts = layout_guts(table)
			glory = contain(*guts)
			write_to_disk(glory)
		finally:
			conn.close()
			print(f"Got the files to the local_machine, boss!")
	else:
		print(f"Something went wrong, boss. Check the connection & config, please.")




