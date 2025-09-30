```python
# install library
pip install mysql_connector
```

```python
import mysql.connector # import relevant packages

# define the connection to MySQL - in reality will be env variables
conn = mysql.connector.connect( # make connection \ call
	host='192.168.x.xxx', # server host IP
	port=3306, # MySQL default
	user='user_name', # the user you defined / created
	password='pass_word', # associated pass for given user
	database='data_base' # name of target db on the server
)

cursor = conn.cursor() # interactive ' mouse '
cursor.execute("SELECT * FROM table_name") # use the cursor to execute cmd
result = cursor.fetchall() # grab all lines returned from query
print(result)

cursor.close() # close the interactive cursor
conn.close() # close connection to remote server / hang up
```
This is the most basic and simplest form of connection to a remote MySQL server. To allow connections from outside the host machine, change the { for macos homebrew installations } /opt/homebrew/etc/my.cnf file from bind_address = 127.0.0.1 to 0.0.0.0, which allows connections from anywhere rather than just the local machine. Likewise, when creating a user to connect under, you should either a. specify the IP address of the client machine or b. set the user to be accepted from anywhere, like so: 
" CREATE USER 'name'@'%' IDENTIFIED BY 'password_' "
Setting the user @ "%" allows any and all locations to connect from. Standard practice is to include an IP address where the "%" is in the Create User command. Then, after creating the user, run FLUSH PRIVILEGES to commit the user's permissions and restart the server with "mysq.server restart" to make the bind_address change take effect. Finally, open the port 3306 on the server's host machine's router to complete the  remote access configuration.

Additional commands and queries:
```python
cursor.execute("SELECT * FROM users")
result = cursor.fetchall() # gets all rows
# or
result = cursor.fetchone() # gets a single row
```
INSERT
```python
cursor.execute("INSERT INTO users (name, email) VALUES ('John', 'johng@gmail.com')
conn.commit() # have to commit the changes to save them
```
UPDATE
```python
cursor.execute("UPDATE users SET email='newemail@gmail.com' WHERE name = 'John'")
conn.commit()
```
DELETE
```python
cursor.execute("DELETE FROM users WHERE name = 'John'")
conn.commit()
```

Connections are Stateful; they exist until closed or dropped by either machine. 

Also, executemany is the same as execute but more efficient for bulk processing. An example of loading several queries into a single var for executemany is below:
```python
data = [
	('user_1','user1@gmail.com'), # make each pair of data
	('user_2','user2@gmail.com'),
	(Thousands more statements)
]

cursor.executemany( # use executemany for efficiency
	"INSERT INTO users (name, email) VALUES (%s, %s)",
	data # the sets of pairs we configured above
)
conn.commit() # single commit for every insert
```

To allow substantial files and transfers, the max_allowed_packet variable might need to be increased. This is done by specification within the connection. The default is usually 1 MB.
```python
conn = mysql.connector.connect( # make connection \ call
	host='192.168.x.xxx', # server host IP
	port=3306, # MySQL default
	user='user_name', # the user you defined / created
	password='pass_word', # associated pass for given user
	database='data_base', # name of target db on the server
	max_allowed_packets=67108864 # raised to 64 MB
)
```
Or could globally set this on the server:
```python
SET GLOBAL max_allowed_packet=67108864;
```
Additional variables:
```python
conn = mysql.connector.connect( # make connection \ call
	#. . . previous variables . . . 
	max_allowed_packets=67108864, # raised to 64 MB
	auto_commit=False, # manual commitments
	connection_timeout=3600 # one hour
)
```

Transaction could also be used for controlled, manual commitments to the db:
```python
conn.start_transaction() # controlled commits

bulk_texts = [
	('title_1', 'long_text_1'),
	('title_2', 'long_text_2'),
	(# many more rows)
]

cursor.executemany(
	"INSERT INTO articles (title, content) VALUES (%s, %s)",
	bulk_texts
)

conn.commit() # write all to disk
```