import os
import pandas as pd
import mysql.connector 
from config import *

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

def find_tables(conn):
	cursor = conn.cursor()

	query = "SHOW TABLES;"
	cursor.execute(query)
	tables = cursor.fetchall()

	return tables
 
 # probably better implementation of querying for tables
 # especially to include the order by clause 

def search_tables(conn):
	cursor = conn.cursor()

	query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{DATABASE_NAME}' ORDER BY table_name DESC;"
	cursor.execute(query)
	tables = cursor.fetchall()

	return tables

if __name__ == "__main__":
	conn = initialize_connection(DB_USER, PASS_PHRASE, DATABASE_NAME, DATABASE_ADDR)

	tables = search_tables(conn)
	print(tables)
	conn.close()














