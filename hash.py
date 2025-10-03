import os
import hashlib

LOCAL_DIR = '/home/tom/vault'

def validate(LOCAL_DIR):
	hashes = []
	for root, dirs, files in os.walk(LOCAL_DIR):
		for filename in files:
			try:
				fll_fpath = os.path.join(root, filename)
				rel_fpath = os.path.relpath(fll_fpath, LOCAL_DIR)
				ftype_ign = ('.DS_Store', '.obsidian', '.git') # move to config file
				hasher = hashlib.sha256()
				
				if any(term in fll_fpath for term in ftype_ign):
					print(f"{filename}\'s spoofed.")
				else:
					with open (fll_fpath, 'rb') as f: # binary
						# walrus assigns & returns variable ":="
						while chunk := f.read(8192):
							hasher.update(chunk)
					guts = hasher.hexdigest() # get all chunks
					hashes.append(guts) # append hash to list
			except Exception as e:
				print(f"Hash generation failed for {filename}: {e}")
	return hashes

def verify(hashes_o, hashes_n):
	try:
		if hashes_n == hashes_o:
			print("Verified.")
		else:
			print("Something's wrong.")
	except Exception as e:
		print("Error with verification")

if __name__=="__main__":
	try:
		hashes = validate(LOCAL_DIR)
		hashes_n = hashes
		hashes_o = hashes
		truth = verify(hashes_o, hashes_n)
	except KeyboardInterrupt:
		print('Cut it off!!')
