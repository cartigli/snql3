import os

DB_USER = os.getenv('DB_USER','notation')
DB_PASS = os.getenv('DB_PASS','0n3*4t!2D*62')
DB_NAME = os.getenv('DB_NAME','notes')
DB_ADDR = os.getenv('DB_ADDR','192.168.1.68') # these could all be without DB_ :(

# LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/vault') # macos - host
LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/vault') # linux - remote
# LOCAL_DIR = os.getenv('LOCAL_DIR','C:\\Users\\carto\\vault') # windows - remote
# LOCAL_DIR = os.getenv('LOCAL_DIR','C:\\Users\\carto\\vault') # windows - remote
# or a raw string for windows pc's cause \ is escape in py
# r'C:\Users\carto\vault'
# technically, '\u', '\c', & '\v' are not escape characters so this specific path would be fine, but something like:
# 'C:\data\temp' would with '\t'
# if on linux/macos, do not worry about this ^

#CLIENT = os.getenv('CLIENT', 'compuir') # macos
CLIENT = os.getenv('CLIENT', 'tom') # linux
#CLIENT = os.getenv('CLIENT', 'cart0') # windows
