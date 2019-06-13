
## Capstone 360 Developer Documentation -- Mock Up Database Information

The purpose of this document is to provide set up information for creating the mock up database for local testing.
The mockup was designed for testing during development of the application with SQLite: https://www.sqlite.org/index.html

The database file should exist in the main capstone360 app directory.
Currently line 14 in app.py, "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'," identifies the location of this temporary database for the application.

#### To create a fresh database file:

1. If 'capstone360.db' exists, remove it. Proceed to the next step otherwise.
2. Run 'python3 /capstone360/setup_mockup_db.py'

#### Adding yourself as a professor

To add yourself as a professor, there are a few means available:

First, you may wish to edit the script such that you're automatically added each time that the database is created.

Currently line 54, 'professors = [("gpld", "George Portland"), ("rdren", "Rick Darren")]' generates this data. Edit this information for your log in and name. An edited file this way should not be committed to the repo.

You also have the option of manually adding yourself to the database:

1. Run sqlite with capstone360.db as the file to edit
2. Run the following SQL command:

INSERT INTO professors (id, name) 
VALUES (<login>,<name>) 

Alternatively, use DB Browser to insert your information (see below)

#### Adding yourself as a student

While it is possible through similar means to add yourself as a student via calls to the database or modifying the set up file, it is ensure you're added as a professor first, and then use the application to add yourself as a student. See /docs_usage_guide.md for more information.

#### Recommended Software:

DB Browser for SQLite: https://sqlitebrowser.org/

I've found this to be a useful application for viewing and modifying the database during development. It allows you to conveniently view through all tables and records, and inserting or updating records are similarly quite easy to perform.





