Interacting with and opening files with Python.

open( ) is a built-in function
```python
open(file_path, access_mode)
```
Access modes: 
	   r = read only
		 w = opens a file to write only, makes a file if doesn't exist

Ok, this is much simpler than I expected

```python
with open(file_path, 'r') as file:
	line_count = 0
	for line in file:
		line_count += 1
	return line_count
```


```python
import os  
  
# Get the current working directory  
current_directory = os.getcwd()  
print(f"Current working directory: {current_directory}")  
  
# List contents of a directory  
contents = os.listdir(current_directory)  
print(f"Contents of current directory: {contents}")

os.walk()
```

```python
import os

for root, dirs, files in os.walk('/Volumes/HomeXx/compuir/vault/xsorted()/III SQL'):
	print(f"{root}, {dirs}, {files}")
```


Count file lengths recursively through a given folder:
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'

line_cnt_list = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			with open(full_file_path, 'r') as file:
				line_count = 0
				for line in file:
					line_count += 1
				line_cnt_list.append(line_count)
		except:
			continue

line_cnt_list.sort()

print(max(line_cnt_list))
print(line_cnt_list)
```

```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'

char_cnt_list = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			with open(full_file_path, 'r') as file:
				char_count = 0
				for line in file:
					char_count += len(line)
				char_cnt_list.append(char_count)
		except:
			continue

char_cnt_list.sort()

print(max(char_cnt_list))
print(char_cnt_list)
```






Count characters recursively through a given folder:
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault/xVault'

char_cnt_list = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			with open(full_file_path, 'r') as file:
				char_count = 0
				for line in file:
					char_count += len(line)
				char_cnt_list.append((char_count, filename))
		except:
			continue

char_cnt_list.sort()

print(max(char_cnt_list))
print(char_cnt_list)
```

7,861,302

Let's make a list of files then commands for MySQL instead of trying to connect the API or manually inserting text.
This one outputs a list of of the files' location within the given dir:
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'

files_dedir = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			files_dedir.append(full_file_path)
		except:
			continue

print(len(files_dedir))
print(files_dedir)
```
*Let's try to make the files be output on a different line for every file on a new line:*
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'
files_dedir = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			print(full_file_path)
		except:
			continue
```
*Ok, close enough, we can make a .py file with these contents and run ' file.py > file_lo.txt ' and the full path for every file in the given directory is printed.*
```python
import os

file_path = ./scpt.txt

for line in file_path,
	print(line)
```


Alright, so the script below prints all the lines of the file one at a time. Much closer.
```python
import os  

file_path = '/Volumes/HomeXx/intel/scpt.txt'

with open(file_path, 'r')as f:
	for line in f:
		print(line, end=' ')
```
*Additionally, with an Auto_Incrementing Primary Key, we don't need a generated number for the iteration when creating the collection of insertion queries.*


Sike, I'm doing too much. That first one is fine, the hell was I thinking?
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'
files_dedir = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			print(f"INSERT INTO n1 (title, notes)\nVALUES ('{filename}', LOAD_FILE('{full_file_path}));")
		except:
			continue
```
*Have this output go to a .sql file and then load it into my workbench for execution. This actually worked incredibly well. The only issue is apostrephies were included in the titles, which confused MySQL. Let's fix it:*
```python
import os

file_path = '/Volumes/HomeXx/compuir/vault'
files_dedir = []

for root, dirs, files in os.walk(file_path):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			if "'" in filename:
				print(f"File name contains an apostrohe:{filename}")
			else:
				print(f"INSERT INTO n1 (title, notes)\nVALUES ('{filename}', LOAD_FILE('{full_file_path}));")
		except:
			continue
```

Now this deals with the two inner files seperatley:
```python
import os

file_path_g = '/Volumes/HomeXx/compuir/vault/xVault'
file_path_s = '/Volumes/HomeXx/compuir/vault/xsorted()'

for root, dirs, files in os.walk(file_path_g):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			print(f"INSERT INTO n1 (title, notes)\nVALUES ('{filename}', LOAD_FILE('{full_file_path}));")
		except:
			continue

for root, dirs, files in os.walk(file_path_s):
	for filename in files:
		full_file_path = os.path.join(root, filename)
		try:
			print(f"INSERT INTO n1 (title, notes)\nVALUES ('{filename}', LOAD_FILE('{full_file_path}));")
		except:
			continue
```