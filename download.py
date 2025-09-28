import os
import pandas as pd
import mysql.connector
from config import *

def survey_db(conn, TABLE_NAME):
	cursor = conn.cursor()
	query = f"SELECT * FROM {TABLE_NAME}"
	cursor.execute(query)
	notes_remote = cursor.fetchall() # one tuple per note from table returned
	return notes_remote

def layout_guts(notes_remote):
	note_name = []
	note_lo = []
	note_guts = []
	for record in notes_remote:
		note_name.append(record[1])
		note_lo.append(record[2])
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
		#name = row['name']
		contents = row['contents']
		directory = os.path.dirname(path)
		os.makedirs(directory, exist_ok=True)
		with open(path, 'w') as f:
			f.write(contents)
