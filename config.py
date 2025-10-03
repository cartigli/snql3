import os

#DB_USER = os.getenv('DB_USER','notation')
#DB_PSWD = os.getenv('DB_PSWD','0n3*4t!2D*62')
#DB_NAME = os.getenv('DB_NAME','notes')
#DB_ADDR = os.getenv('DB_ADDR','192.168.1.68')

DB_USER = os.getenv('DB_USER','root')
DB_PSWD = os.getenv('DB_PSWD','koipo222')
DB_NAME = os.getenv('DB_NAME','notes')
DB_ADDR = os.getenv('DB_ADDR','localhost')

LOCAL_DIR = os.getenv('LOCAL_DIR','/Volumes/HomeXx/compuir/vault') # macos - server host
#LOCAL_DIR = os.getenv('LOCAL_DIR','/home/tom/vault') # linux - remote
