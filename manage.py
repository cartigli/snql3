import os
import time
import datetime
import pandas as pd
import mysql.connector
from config import *

def survey_db(conn, DB_NAME):
	cursor = conn.cursor()

	q = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{DB_NAME}' ORDER BY table_name DESC;"
	cursor.execute(q)

	tables = cursor.fetchall()

	return tables

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


if __name__=="__main__":
	uploads = []
	uploads.append("Current uploads available to pull:") # so first item is index: 1
	# user's choice to pull - 1 = the element indice of the table to be downlaoded from {tables}

	conn = initialize_connection(DB_USER, DB_PSWD, DB_NAME, DB_ADDR)
	results = survey_db(conn, DB_NAME)
	conn.close()

	for result in results:
		raw = str(result[0]).replace('plus','+').replace('less','-')
		clean = raw.replace('de','').replace('_','')

		try:
			dt = datetime.datetime.strptime(clean, '%Y%m%d%H%M%S%z')
			uploads.append(dt)

		except ValueError:
			try:
				dt = datetime.datetime.strptime(clean, '%Y%m%d%H%M%S')

			except ValueError as e:
				print(f"Could not parse dt_obj {raw}; {e}")

	try:
		for i, item in enumerate(uploads):
			print(f"{i}:{item}")

	except Exception as e:
		print(f"Uh-oh Boss; {e}")