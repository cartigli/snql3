import os
import pandas as pd
import mysql.connector
from config import *


def survey_db(conn, TABLE_NAME):
	cursor = conn.cursor()
	query_0 = f"SELECT * FROM {TABLE_NAME};"
	cursor.execute(query_0)
	notes_remote = cursor.fetchall()

	#query_1 = f"SELECT client FROM meta;"
	#cursor.execute(query_1)
	#client = cursor.fetchone()

	return notes_remote

 
def layout_guts(notes_remote):
	note_name = []
	note_lo = []
	note_guts = []
	patched_path = []

	for record in notes_remote:
		note_name.append(record[1])

		rel_path = record[2]
		new_path = os.path.join(LOCAL_DIR, rel_path)
		#new_path = old_path.replace(old_base, LOCAL_DIR)
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


# copied from upload - identical
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


if __name__ == "__main__":
	conn = initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, DATABASE_ADDR)
	if conn:
		try:
			notes_remote = survey_db(conn, TABLE_NAME)
			guts = layout_guts(notes_remote)
			glory = contain(*guts)
			write_to_disk(glory)
		finally:
			conn.close()
			print(f"Got the files to the local_machine, boss!")
	else:
		print(f"Something went wrong, boss. Check the connection & config, please.")




