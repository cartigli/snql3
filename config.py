import os

DB_USER = os.getenv('DB_USER','notation')
PASS_PHRASE = os.getenv('PASS_PHRASE','0n3*4t!2D*62')
DATABASE_NAME = os.getenv('DATABASE_NAME','notes')
DATABASE_ADDR = os.getenv('DATABASE_ADDR','192.168.1.68')

# LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/vault') # macos - host
LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/vault') # linux - remote
# LOCAL_DIR = os.getenv('LOCAL_DIR','C:\\Users\\carto\\vault') # windows - remote
# or a raw string for windows pc's cause \ is escape in py
# r'C:\Users\carto\vault'

# for a simple commit history by machine - client
#CLIENT = os.getenv('CLIENT', 'compuir') # macos
CLIENT = os.getenv('CLIENT', 'tom') # linux
#CLIENT = os.getenv('CLIENT', 'cart0') # windows
