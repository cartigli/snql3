import os
import pandas as pd
import mysql.connector
from config import *


def survey_db(conn, NAME):
	cursor = conn.cursor()

	q = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{NAME}' ORDER BY table_name DESC;"
	cursor.execute(q)

	tables = cursor.fetchall()
	table = tables[0][0]

	return table


def survey_t(conn, table):
	cursor = conn.cursor()

	q = f"SELECT * FROM {table};"
	cursor.execute(q)
	guts = cursor.fetchall()

	return guts

 
def layout_guts(guts):
	note_name = []
	note_lo = []
	note_guts = []
	hashes = []

	for record in guts:
		note_name.append(record[1])

		rel_path = record[2]
		new_path = os.path.join(LOCAL_DIR, rel_path)
		repaired_path = os.path.normpath(new_path) # win
		note_lo.append(repaired_path)

		note_guts.append(record[3])

		hashes.append(record[4])

	return note_name, note_lo, note_guts, hashes


def contain(note_name, note_lo, note_guts):
	notes = pd.DataFrame({
			'name': note_name,
			'path': note_lo,
			'contents': note_guts,
			'hashes': hashes
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


def initialize_connection(DB_USER, DB_PSWD, DB_NAME, DB_ADDR):
	try:
		conn = mysql.connector.connect(
			host=DB_ADDR,
			user=DB_USER,
			password=DB_PSWD,
			database=DB_NAME
		)

		return conn
		
	except Exception as e:
		print(f"ERR: {e}; CHECK CONFIG!")

		return None


if __name__ == "__main__":
	conn = initialize_connection(DB_USER, DB_PSWD, DB_NAME, DB_ADDR)

	if conn:
		try:
			table = survey_db(conn, DB_NAME)
			contents_detable = survey_t(conn, table)
			note_name, note_lo, note_guts, hashes = layout_guts(contents_detable)
			glory = contain(note_name, note_lo, note_guts)
			write_to_disk(glory)
		finally:
			conn.close()
			print(f"Got the files to the local_machine, boss!")
	else:
		print(f"Something went wrong, boss. Check the connection & config, please.")
