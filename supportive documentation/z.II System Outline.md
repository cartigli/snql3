What I want the system to <u>do</u>.

Configuration File
	A configuration file in the project directory contains the target folder, some authentication for the MySQL server, IP address and key for location of server as well, database / table of the backup

The main application logic will check the configuration file for the local directory to be backed up. If no folder is specified or the folder does not exist on this machine, the process should exit with a message stating the issue found.

If exists and contains .md files, the application will take the folder and create a series of queries for the SQL server to load the given files from the specified folder into the database. *Can Load File be used when remote? I don't think it can. I'm pretty sure we'll need to find another way to send the notes to the server, potentially using the host machine as a relay. But I also bet the API has something for this. We'll come back.* **It cannot.**

The Insert queries generated should include the necessary tables and related values with their respective formats for each column. As of now, this will be Insert into notes (note_no, title, path, note, creation_date, last_edit_date) VALUES(Int auto_increment primary key, varchar(75) not null, varchar(255) not null, Text not null character set utfmb64, date format 'mm-dd-yyyy 00:00:00.00'). 

After making the queries for every file in the folder, ignoring all the files that do not end in .md, the application checks to see if the database and table exists under the names specified in the configuration file. If yes, it proceeds but if either are not, it will exit stating the error to the user.

Alright, consider classes and functions. We need to search files and collect information with the File Manager, connect and authenticate with the Server Associate, and push & pull to & from the database with the Server Liaison. Maybe build queries with the Contractor, but this could be blended in or out of another class. We'll see.

Classes: File Manager { 1 }, Server Associate { 2 }, Server Liaison { 3 },  Contractor { 4 }

File Manager Class { }
This class is responsible for the finding of all files, the identification, recording, and organization of the local machines files to be backed up. It will need to find all the .md files' location, filename, and contents, as well as the Timestamp of creation & the last edit. Let's leave this out for now as dealing with os's and metadata divergence will be tedious.

Server Associate Class { }
This class will ensure the MySQL server specified in the configuration file is up, running healthily, and accepting of the authentication, also given in the configuration file.

Server Liaison Class { } 
I have not quite figured out how I will do this one. With local files and directories, LOAD_FILE('file_path') suffices, but when remote, it will not. The official, supported method of communication with a MySQL instance is the Python Connector, which uses an API. This would technically work, but I expect difficulties and additional trouble shooting when attempting to upload 50,000+ characters in a single text file over this API. I suppose we will see.

Contractor Class { }
Depending on the method we decide to do, this class will serve the role of building the queries to be executed. For example, once we collect the filename, filepath, title, and timestamps, we will need a simple loop to iterate through the files found and create a .sql file containing every insert statement and create statement[s] if needed. Also, we will need filtering or error handling if single quotations or apostrophes are used in any titles. If it is, be sure to check the paths as well as the ill-configured filename will be there as well.

Configuration File
This will need to hold the following for authentication with a given user who exists in the database:
	_ user
	_ pass_phrase
	_ data base surname
	_ table if already exists or otherwise needed
	_ server IP
	_ server_host port No