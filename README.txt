This code was inspired by Github's architecture and designed for private, self-hosting of .md files. 
This code was inspired by Github's architecture and designed for private, self-hosting of .md files. 

I use an obsidian vault for *everything* and needed a place to backup the collection of information I had created over the years. Github was an obvious candidate for its simplicity and reliability, but with the glaring downside of leaving my notes on a third party's servers. Although I could encrypt repositories with git-crypt or ignore sensitive files, this still either leaves the information (albeit encrypted) on remote hardware or doesn't backup the sensitive information. Even with a private repository, leaks do happen and Github is not perfect.

These scripts allow a user to backup a specified folder and its contents in a given MySQL server. The current architecture ignores almost all file-types outside of .md files, but this can be easily changed in the upload.py script. The backup consists of the folder's notes, each note specified as a unique record in the table with columns for the title, relative path within the given directory, and contents of said note. 

Every time the upload script is run, a new table is generated with a title that includes the UTC timestamp from when the table is created. Within this architecture, the download script can merely order the output by the values of the tables' titles in a given database and choose the first item. Then, this item is specified as the table to 'Select * From . . .' which ensures only the most recent uploaded vault is downloaded or 'pulled'. 

*Also, the relative path from the uploaded notes are joined to the given Local_Dir variable from the host machine's env file, ensuring that if machines change from upload to download, the change in path is automatically resolved and the original structure is rebuilt within the specified Local_Dir.*

*Additionally, os.path.normpath() is applied to the result of the join of the rel_path and Local_Dir to repair potential conflicts of separators, i.e., "\" and "\" when switching from Macos or Linux based os's to windows, which uses backslashes instead of forward slashes. In python, this is dangerous as backslashes dictate escaped characters and would cause errors if a Linux or Macos path was joined with a Local_Dir of 'C:\Users\carto\vault', for example. Cross platform between Macos and Linux has been tested, but **not** between either of these platforms and Windows.*

The overall structure is fairly simplistic. It is split into three main scripts that a user would need to modify before use. They are the upload, download, and config scripts. They do the following:

upload.py:
	Takes a given directory and walks through the entire contents. For every filename in the files found from the walk, the script initially prints an ignore statement for the ignored files: any file that contains any of these strings at any point within the full path of the given file-path is ignored: .DS_Store, .obsidian, .git. This is like a simplistic .gitignore, although I do feel more comfortable relying on this function to ignore the required files than when using .gitignore. {Soon, I'd like to refactor these strings to the config file for convenience.} 
	Then, for everything besides what was just ignored, the given file's name, path {relative}, and contents are each added to their respective lists. These three lists are returned, and then repackaged into a single pandas DataFrame, which is then modified by the .to_records() function, and returned.
	Next, connection to the mysql.server is established and returned. It is used to execute two queries for the database, one to make the table with the prefigured values and var_types {titled with the UTC timestamp} and the other to insert the values collected, and currently in a pd.DataFrame, into the new table, ensuring one record per note with Not Null enforced with every column on the new table. The new insertions are committed, and the connection is closed.

download.py:
	initializes identical connection, but uses it to find all the tables from the db in the config file. These are Ordered By table_name in Desc order, which allows us to merely select the first item returned from this Select statement and use it as the table name to pull the vault from. 
	*Since tables are only ever titled with the same exact formatting and UTC generation function, we know several things: The higher the value, the more recent the upload. The highest value will be the most recent upload. And finally, the only possibility that could create conflicts at any point would be if two people uploaded folders to the same db at the exact same second exactly. For every other scenario, no conflicts will be seen and it will be clear which upload was done the most recently.*
	With the most recent table found, the script selects everything within said table and applies the reverse list organization as upload.py. The tuple containing all the notes from the table is iteratively cycled through by record and appends the note's name and contents to empty lists made for their contents. The path is found/made by joining the Local_Dir variable from the config file with the rel_path found from the table. and appended to its respective list, resulting in three lists containing every files name, full path for the local machine, and contents.
	Finally, with the same connection we are well accustomed to, the download script unpacks the collected note's full local path and contents. The path is used for os.path.dirname which identifies the directories/sub-directories from a given path. Then, os.makedirs takes the given output from os.path.dirname and creates the given directories and sub-directories {exists_ok=True here ensures the script continues w/o error if a given directory or sub-directory already exits}. Lastly, the path is used for with open(path . . . to write the contents of a given epoch's specific file and the connection is closed.

config.py:
	This is the env file containing the sensitive and likely evolving components of the connection to the MySQL server & database. The most important components for making the connection are below:
		db_user: this should be the user you created on your MySQL server { you need to make a user to do this }
		pass_phrase: when you make a new user, you need to specify a password for the user. MySQL is frustratingly strict on password strength, btw. Whatever it ends up being, ensure it is correctly copied here.
		db_name: Specifying the db_name here allows connection to and interaction specifically within one db, limiting scope and range of possible damage or alteration.
		db_addr: this is just the ip addr of the host machine of the MySQL server. MySQL uses port 3306 by default so unless you specifically modified this within the configuration *of MySQL*, it does not need to be specified.
	These are all the MySQL env variables ^ needed for connection and authentication. Below are additional specifications needed for the application's functionality.
		Local_Dir: this is the full path of the folder on your current machine that you want to upload to the db. Again, this has been tested successfully across Macos and Linux machines, but as of the time I am writing this {9.29.25.11.06}, it has not been tested.
		Client: this is deprecated and will likely be removed in a future push. It was used as identification of *who* uploaded which files, but was removed during a refactoring of the path and feels pretty extraneous. Personally, I don't care about having this record but we will see where progress takes us.


Making a user
This was a huge pain for me but is actually simple, i just kept cutting corners. The generic command is:
```mysql
CREATE USER 'username'@'user_ip_addr' IDENTIFY BY "your-strong-pass";
```
As mentioned previously, the password's requirements in MySQL are strict; the password will need to be fairly complex. Also, the user_ip_addr is very important. If on the machine hosting the MySQL server, this should be 'localhost' or '127.0.0.1'. If connecting from any other machine, the user_ip_addr should either be the remote {even if on the same network} machine's ip_addr OR one could denote the ' any - origin ' authentication for this user by specifying with: 'username'@'%' which allows connections of that user from any ip_addr.

This is half the battle. Now, we must grant permissions on the new user we just created. Initially, this must be done through the root shell of the server, found with 'mysql -u root -p'. Once inside and authenticated as root, run the following commands:
```mysql
GRANT PRIVILEGES ALL ON db_name.* TO 'new_user'@'%';
FLUSH PRIVILEGES;
```
*If you do not flush the privileges while in the root terminal of the server, the user's permissions will **not** be granted.*


Making MySQL listen:
MySQL only listens to local host by default, so connection from outside the host is restricted. To change this, you must modify the MySQL conf file {located at /opt/homebrew/etc/my.cnf for brew installations on macos} to include these lines:
```mysql
bind-address = 0.0.0.0
mysqlx-bind-address = 0.0.0.0
```
*I am fairly certain that mysqlx-bind-address doesn't need to specified here, especially with bind-address included, but it is good practice. Also, 0.0.0.0 means listening on all interfaces. If you only had one machine to interact with the server, specifying its IP address here would be a much more secure practice.*

Also, to allow MySQL to read files on the host machine, if you wanted to use MySQL's functions for reading files, you must also include this line:
```mysql
secure-file-priv = ""
```
Or, you could put a folder inside the quotations to restrict MySQL's access to only that folder. This was helpful for me initially when learning how MySQL works with data like strings of 40,000+ characters. Not so much for remote work or anything else as far as I have seen, just good to know.

After either of the above modifications are made to the my.cnf file, restart the server with "mysql.server restart" {at least for Macos - homebrew instances}. The modification will not take effect until this is done.