## Capstone 360 Developer Documentation
This is the main documentation for developers and anyone who maintains the Capstone 360 application.

### Getting Started
This application is a flask based web app running on a PSU CAT virtual machine.  The Postgres database is also hosted by the CAT.  

### Requirements
- Python
- Flask
- Flask-CAS
- Sql Alchemy

### Overview

#### Install and Running
Clone the repo
```
git clone git@github.com:capstoneteamb/capstone360.git
```
Go to the cloned repo directory and run:
```
python app.py
```

### Web App Structure
This webapp follows the Model View Controller architectural pattern.
- Model -- gbmodel directory
	- these py files will make database calls for the webapp which processes user data and passes results to the view.
- View -- template directory
	- these static files will handle the display of the webapp with styling and user interaction functionality
- Controller -- various .py files
	- these files contains the main functionality of the webapp.  These files are responsible for the application logic and is the middleman between the View and Model

#### gbmodel Directory
##### model_sqlalchemy.py
The model_sqlalcehmy.py file contains functions to make calls to the Postgres database.

#### static Directory
This contains all CSS, Javascript and static images files.

#### template Directory
This contains all the html files for the web app.  These templates uses the jinja2 templating engine, for further resources on jinja2 go to http://jinja.pocoo.org/

#### main directory

##### app .py

This is the main .py file for the capstone360 application.  This file is where the flask framework is instantiated and also contains most of the imports and routes for the webapp.  The CAS configuration is also setup in this file.

##### catCas .py
This file uses CAS to get the username from CAT and validates if the user exists in the database.

There are two functions:
: ###### validate_students()
: --takes the CAS.username and looks if its the student table

: ###### validate_professors()
: --takes the CAS.username and looks if its in the professor table

##### form .py
This file handles the form and writes to the database when a user fills out a review. 
This file adds the form functionality for the webapp for students to fill out their midterm and final reviews. 

##### index .py
This file is the placeholder to render index.html

##### prof_dashboard.py

This file contains the implementation and functionality of the professor dashboard which includes add/remove students/team, add new sessions, set review of midterm/final start/end dates and set team lead, and add team by CSV file.

##### report.py

This file will get student reviews from the database and create a report for the instructor to print.

##### student.py

This file contains the implementation and functionality of the student dashboard which includes editing of student email and name.

##### view_student.py

This file contains the implementation and functionality of the student page which displays the midterm and final review for the students which is accessible through the professor dashboard.

##### student_register.py

This file contains the implementation and functionality of the register student page, which allows the a student to register for a capstone session.

##### Connection to the 360 Capstone Webapp

Need to use a VPN or be located on campus to access the 360 capstone webapp.  For further VPN help go to cat.pdx.edu.

#### Adding functionality

If the functionality is similar or related to a current controller file, then add the new function/class to that file, make sure to return what is needed to the corresponding View file.  
*Note - Do not add database calls to the controller file, add it to the model.

If the functionality is different then:
- Create a route in app.py and make sure it references a html file that will be the view.
- Put database calls to the model file.

#### Adding students to the database using database calls

Database login when connected to a VPN:
```
psql -h db.cecs.pdx.edu database_name database_name
```
Replace database_name with the actual name of the database

Use this database call to add professors to the Postgres database:
Replace user_id with the student id

```
INSERT INTO students (id, tid, session_id, name, is_lead, midterm_done, final_done, active, email_address)
VALUES ('user_id',1,0,'name here',0,0,0,'midterm', 'email here');
```


#### Adding professor to the database using database calls

Use this database call to add professors to the Postgres database:
Replace user_id with the professor id
```
INSERT INTO professors (id, name) VALUES ('user_id', 'name here');
```

### Note for Flask-CAS extension
Modify routing.py in the Flask-CAS extension folder.
Comment out line 125 and add line of code below.
```python
125     #attributes = xml_from_dict["cas:attributes"]
126     attributes = xml_from_dict.get("cas:attributes",{})
```

## License
MIT