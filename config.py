import os

DB_USER = os.getenv('DB_USER','notation')
PASS_PHRASE = os.getenv('PASS_PHRASE','0n3*4t!2D*62')
DATABASE_NAME = os.getenv('DATABASE_NAME','notes')
TABLE_NAME = os.getenv('TABLE_NAME','notes_2') # let's have this be a timestamp or similar
DATABASE_ADDR = os.getenv('DATABASE_ADDR','192.168.1.68')

LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/vault') # macos - host
# LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/fr/vault') # linux - remote
# LOCAL_DIR = os.getenv('LOCAL_DIR','C:\\Users\\carto\\vault') # windows - remote
# or a raw strong for windows pc's cause \ is escape in py
# r'C:\Users\carto\vault'

# for a simple commit history by machine - client
CLIENT = os.getenv('CLIENT', 'compuir') # macos
#CLIENT = os.getenv('CLIENT', 'tom') # linux
#CLIENT = os.getenv('CLIENT', 'cart0') # windows