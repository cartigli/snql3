import os
import pandas as pd
import mysql.connector 
from config import *

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
		print(f"ERR {e}: CHECK CONFIG")

		return None

#def find_tables(conn):
#	cursor = conn.cursor()
#	query = "SHOW TABLES;"
#	cursor.execute(query)
#	tables = cursor.fetchall()
#	return tables 
 # probably better implementation of querying for tables
 # especially to include the ORDER BY clause
 # also, this 'tables' list is a collection of tuples

def search_tables(conn):
	cursor = conn.cursor()

	query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{DB_NAME}' ORDER BY table_name DESC;"
	cursor.execute(query)
	tables = cursor.fetchall()

	table = tables[0][0]
	
	return table

if __name__ == "__main__":
	conn = initialize_connection(DB_USER, DB_PSWD, DB_NAME, DB_ADDR)

	table = search_tables(conn)
	#print(tables) # list of tuples
	print(table) # prints only youngest table based off the timestamps relative to other tables
	conn.close()

# Now that we can reliably find the largest title of any 
# table in the given db, and it is returned as a string, 
# we can now modify the download script to download only 
# the table with the largest value in its title, which 
# will {coming soon} be a UTC timestamp, enforcing and 
# ensuring only the most recent vault is downloaded from 
# the db. Addditionally, this will allow us to make a new 
# table for every upload, each one described by its  
# timestamp origin and possibly upload client. This helps 
# conflicts an allows for backups without truncation or 
# overwriting.