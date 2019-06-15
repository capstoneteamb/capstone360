
## Capstone 360 Developer Documentation -- Usage Guide

### Setting Up the Database

#### [Note: This is to create a new database. As such, it will remove out the old one including all its data. Please ensure that you wish to re-create the database before taking this step and have backed up any data you wish to save]

1. Go to the capstone360 directory
2. From the command line, enter 'service apache2 restart' [This will clear any previous connection to the db which may be blocking the set up from proceeding.]
3. In the command line, enter 'python3 create_db.py' *Danger: This will wipe out the old database tables including their contents as this is necessary to create the tables. Only proceed with this step if you wish to wipe out the old data.*
4. You will now have a fresh database.
5. For good measure, enter 'service apache2 restart' again

Note: If step 2 is skipped, the process may hang. If so, use 'ps' from the command line to find the python process running and enter 'kill <pid>'

### Inserting Yourself as a Professor Into the Database

#### [Note: Anyone entered into the database in this way will have full access to the application and its contents]

1. Go to the capstone 360 directory
2. From the command line, enter 'python3 insert_prof.py'
3. At the first prompt, enter your MCECS log in
4. At the next prompt, enter your name

### Removing Yourself as a Professor From the Database

#### [Note: Removing your log in will remove your access to the professor side of the application and its contents]

1. Go to the capstone 360 directory
2. From the command line, enter 'python3 remove_prof.py'
3. At the prompt, enter the MCECS log in you wish to remove


