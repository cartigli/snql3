import os

DB_USER = os.getenv('DB_USER','notation')
PASS_PHRASE = os.getenv('PASS_PHRASE','0n3*4t!2D*62')
DATABASE_NAME = os.getenv('DATABASE_NAME','notes')
TABLE_NAME = os.getenv('TABLE_NAME','notes_2')
DATABASE_ADDR = os.getenv('DATABASE_ADDR','192.168.1.68')
HOST_PORT = os.getenv('HOST_PORT','3306')

LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/Desktop/vault_test')
