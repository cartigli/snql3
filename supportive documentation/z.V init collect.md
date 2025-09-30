```python
import os
import pandas as pd

LOCAL_DIR = '/Volumes/HomeXx/compuir/vault' # env variable

def collector(LOCAL_DIR):
	folder_path = LOCAL_DIR
	guts_togo = []
	name_togo = []
	lo_togo = []
	spoofed = []
	add_err = []
	for root, dirs, files in os.walk(folder_path):
		for filename in files:
			try:
				fll_fpath = os.path.join(root, filename)
				ftype_ign = ('.DS_Store', '.obsidian', '.git')
				if any(term in fll_fpath for term in ftype_ign):
					spoofed.append(filename)
					print(f"{filename}\'s spoofed.")
				else:
					with open (fll_fpath, 'r', encoding='utf-8') as f:
						guts = f.read()
						guts_togo.append(guts)

					lo_togo.append(fll_fpath)
					name_togo.append(filename)
			except UnicodeDecodeError:
				print(f"ENCODING ERR: {filename}.")
				add_err.append(filename)
				continue
			except FileNotFoundError:
				print(f"FILE NOT FOUND: {filename}.")
				add_err.append(filename)
			except PermissionError:
				print(f"PERMISSION ERR: {filename}.")
				add_err.append(filename)
			except Exception as e:
				print(f"ERR {e}: {filename}.")
				add_err.append(filename)

	return guts_togo, name_togo, lo_togo

def container(guts_togo, name_togo, lo_togo):
	guts_glory = pd.DataFrame({
		'note_tl': name_togo,
		'note_lo': lo_togo,
		'note': guts_togo
		})
	ensemble = guts_glory.to_records()
	return ensemble


collected = collector(LOCAL_DIR)
guts = container(*collected) # unpack the collected, contain
print(guts)
```