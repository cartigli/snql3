import os
import hashlib
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

	q = f"SELECT * FROM {table};"
	cursor.execute(q)
	guts = cursor.fetchall()

	return guts

 
def layout_guts(guts):
	note_names = []
	note_relos = []
	note_los = []
	note_guts = []
	hashes = []

	for record in guts:
		note_names.append(record[1])

		rel_path = record[2]
		new_path = os.path.join(LOCAL_DIR, rel_path)
		repaired_path = os.path.normpath(new_path) # win
		note_relos.append(rel_path)
		note_los.append(repaired_path)

		note_guts.append(record[3])

		hashes.append(record[4])

	return hashes, note_names, note_relos, note_los, note_guts


def local_hash(LOCAL_DIR):
	names_local = []
	los_local = []
	hashes_local = []

	for root, dirs, files in os.walk(LOCAL_DIR):
		for filename in files:
			try:
				fll_fpath = os.path.join(root, filename)
				rel_fpath = os.path.relpath(fll_fpath, LOCAL_DIR)

				ftype_ign = ('.DS_Store', '.obsidian', '.git') # should move to config file

				hasher = hashlib.sha256()
				if any(term in fll_fpath for term in ftype_ign):
					#print(f"{filename}\'s spoofed.")
					continue

				else:
					with open(fll_fpath, 'rb') as g:
						while chunk := g.read(8192):
							hasher.update(chunk)

					h_sh = hasher.hexdigest()
					hashes_local.append(h_sh)

					names_local.append(filename)
					los_local.append(rel_fpath)

			except Exception as e:
				print(f"ERR: {e} ON {filename}.")
			except KeyboardInterrupt:
				print(f"Boss cut us off @: {filename}.")
			except Exception as e:
				print(f"Hash generation failed for {filename}: {e}")

	return hashes_local, names_local, los_local


def hash_duty(hashes_local, los_local, hashes, note_relos):
	created = []
	deleted = []
	edited = []

	local_hp = {lo_local: hashe_local for lo_local, hashe_local in zip(los_local, hashes_local)}
	remote_hp = {note_lo: hashh for note_lo, hashh in zip(note_relos, hashes)}

	print(f"Checking files added/removed from server since last upload:")

	for key in local_hp:
		if key not in remote_hp:
			print(f"{key} was deleted or moved.")
			deleted.append(key)
	for key in remote_hp:
		if key not in local_hp:
			print(f"{key} was created or renamed.")
			created.append(key)

	print(f"Checking hashes for edits since last upload:")

	for key in remote_hp:
		if local_hp[key] != remote_hp[key]:
			print(f"Hash discrepancy: {local_hp[key]}:{remote_hp[key]}\n{key} has been edited.")
			edited.append(key)
	
	return deleted, created, edited


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
		print(f"Err: {e}; CHECK CONFIG!")

		return None


if __name__ == "__main__":
	conn = initialize_connection(DB_USER, DB_PSWD, DB_NAME, DB_ADDR)

	if conn:
		try:
			table = survey_db(conn, DB_NAME)
			contents_detable = survey_t(conn, table)
			hashes, note_names, note_relos, note_los, note_guts = layout_guts(contents_detable)
			hashes_local, names_local, los_local = local_hash(LOCAL_DIR)
			alterations = hash_duty(hashes_local, los_local, hashes, note_relos)
		finally:
			conn.close()

	else:
		print(f"Something went wrong, boss. Check the connection & config, please.")