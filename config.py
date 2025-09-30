import os

DB_USER = os.getenv('DB_USER','notation')
DB_PASS = os.getenv('DB_PASS','0n3*4t!2D*62')
DB_NAME = os.getenv('DB_NAME','notes')
DB_ADDR = os.getenv('DB_ADDR','192.168.1.68') # these could all be without DB_ :(

# LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/vault') # macos - host
LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/vault') # linux - remote

#CLIENT = os.getenv('CLIENT', 'compuir') # macos
CLIENT = os.getenv('CLIENT', 'tom') # linux
#CLIENT = os.getenv('CLIENT', 'cart0') # windows