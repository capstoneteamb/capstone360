# File: setup-mockup-db.py
# Date: 3/12/2019 (somewhere around there it was first created)
# Purpose: generate a mockup database with SQLLite

import sqlite3, copy

# Needed to generate student data
names = [
        "John Glover",
        "Ruth Geraldson",
        "Ron Windler",
        "Everet Stinson",
        "Paula Field",
        "Tiberias Rayhen",
        "Kaylin Rhen",
        "Brandan Slater",
        "Deric Chandler",
        "Ryan Jonathan",
        "Rita Slovac",
        "Irene Novac",
        "Paul Photon",
        "Ira Halep",
        "Guy Gregory II",
        "Simona Crison",
        "Hayles Eren",
        "Guy Wilson",
        "Daniel Wilson",
        "Jacob Paulson",
        "Aurel Elric",
        "Ada Green",
        "Ryan Ghan",
        "AJ Breyer-Mugnhen",
        "Emily Manson",
        "Karen Elric",
        "Andy Teran",
        "Leeroy McClain",
        "Erin Wells",
        "Paulson Brown",
        "Charlier Christopher",
        "Adam Polson",
        "Lee Henderson",
        "Adam Nguyen",
        "Karen Barber",
        "Deric Montag",
        "LeAnn Bronson",
        "Ruth Farrari"
]

# Needed to keep track of what team member is on what team
teams = {
        "Team 1": [],
        "Team 2": [],
        "Team 3": [],
        "Team 4": [],
        "Team 5": [],
        "Team 6": []
}

# An example report to base the midterm adn final reports off of
example_report = {
        "time": 1,
        "session_id": 2,
        "tech_mastery": 1,
        "work_ethic": 2,
        "communication": 3,
        "cooperation": 4,
        "initiative": 5,
        "team_focus": 1,
        "contribution": 2,
        "leadership": 2,
        "organization": 3,
        "delegation": 3,
        "points": 4,
        "strengths": "Everything. You are good at everything. There isn't a single problem. Nope.",
        "weaknesses": "So there are a couple of things. One being your sense of humor. Another being your inability and lack of willingness to yodel loudly in public places for no given reasons.",
        "traits_to_work_on": "Yodeling, Kool-Aid style, wall destroying runs, and your decisions to repeatedly press the button for the floor you want to go to when on the elevator--it doesn't make it go faster.",
        "proud_of_accomplishment": "yes?"
}

### Generate Student Data ###
id_num = 0
team_num = 1
student_data = []
for name in names:
    # Generate email address
    split_names = name.split(' ')
    email_address = split_names[0] + "." + split_names[1] + ".notreal@pdx.edu"
        
    # Get student id
    student_id = id_num
    id_num = id_num + 1

    # Get team number
    team_number = team_num
    if (team_num == 6):
        team_num = 1
    else:
        team_num = team_num + 1

    # Add Data To List
    student_data.append((name, email_address, student_id, team_number))
    teams["Team " + str(team_number)].append(student_id)

### Create database and add tables ###
# Connect to database
connection = sqlite3.connect('mockup-database.db')
cursor = connection.cursor()

# Create Capstone Session Table
cursor.execute('CREATE TABLE capstone_session( id INTEGER PRIMARY KEY, start_term VARCHAR(10), start_year VARCHAR(4), end_term VARCHAR(10), end_year VARCHAR(4) );')
cursor.execute('INSERT INTO capstone_session VALUES(?,?,?,?,?)', (2, "winter", 2019, "spring", 2019))

# Create Teams Table
cursor.execute('CREATE TABLE teams( id INTEGER PRIMARY KEY, session_id INTEGER REFERENCES capstone_session(id), name VARCHAR(128) );')
team_list = [
        (1, 2, "Team 1"),
        (2, 2, "Team 2"),
        (3, 2, "Team 3"),
        (4, 2, "Team 4"),
        (5, 2, "Team 5"),
        (6, 2, "Team 6")
]
cursor.executemany('INSERT INTO teams VALUES(?,?,?)', team_list)

# Create Students Table
cursor.execute('CREATE TABLE students( id VARCHAR(20), tid INTEGER REFERENCES teams(id), session_id INTEGER REFERENCES capstone_session(id), name VARCHAR(128), midterm_done BOOLEAN, final_done BOOLEAN, PRIMARY KEY (id, session_id) );')

# Create Team Members table
cursor.execute('CREATE TABLE team_members( tid INTEGER REFERENCES teams(id), sid VARCHAR(20) REFERENCES students(id), session_id INTEGER REFERENCES capstone_session(id), PRIMARY KEY (tid, sid, session_id) );')

# Create Reports table
cursor.execute('CREATE TABLE reports( time TIME, session_id INTEGER REFERENCES capstone_session(id), reporting VARCHAR(20) REFERENCES students(id), tid INTEGER REFERENCES teams(id), report_for VARCHAR(20) REFERENCES students(id), tech_mastery INTEGER, work_ethic INTEGER, communication INTEGER, cooperation INTEGER, initiative INTEGER, team_focus INTEGER, contribution INTEGER, leadership INTEGER, organization INTEGER, delegation INTEGER, points INTEGER, strengths VARCHAR(4096), weaknesses VARCHAR(4096), trait_to_work_on VARCHAR(4096), what_you_learned VARCHAR(4096), proud_of_accomplishment VARCHAR(4096), is_final BOOL, PRIMARY KEY (reporting, tid, report_for, is_final) );')

### Add student and student data to database ###
num_students = len(student_data)
num_teams = len(teams)
for student in student_data:
    # Add Student to students table
    cursor.execute('INSERT INTO students VALUES(?,?,?,?,?,?)', (student[2], student[3], 2, student[0], False, False))

    # Add Student to Team Members Table
    cursor.execute('INSERT INTO team_members VALUES(?,?,?)', (student[3], student[2], 2))

    # Create mock midterm report template from example report
    midterm = copy.deepcopy(example_report)
    midterm["reporting"] = student[2]
    midterm["tid"] = student[3]
    #midterm["report_for"] = 0
    midterm["is_final"] = False
    midterm["what_you_learned"] = ""

    # Create mock final report template from midterm report template
    final = copy.deepcopy(midterm)
    final["is_final"] = True

    # Go through each student who should be on the current student's teams
    for id_number in teams["Team " + str(student[3])]:
        # Create midterm and final reports (that will actually go into the database)
        new_midterm = copy.deepcopy(midterm)
        new_final = copy.deepcopy(final)
        new_midterm["report_for"] = id_number
        new_final["report_for"] = id_number
        if (id_number == str(student[2])):
            new_final["what you learned"] = "This is for myself... I learned how to make a web app. Yah!"
        
        # Debug
        #print (new_midterm)
        #print (new_final)
        #print()

        # Submit Midterm
        cursor.execute('INSERT INTO reports VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (0, 2, new_midterm["reporting"], new_midterm["tid"], new_midterm["report_for"], new_midterm["tech_mastery"], new_midterm["work_ethic"], new_midterm["communication"], new_midterm["cooperation"], new_midterm["initiative"], new_midterm["team_focus"], new_midterm["contribution"], new_midterm["leadership"], new_midterm["organization"], new_midterm["delegation"], new_midterm["points"], new_midterm["strengths"], new_midterm["weaknesses"], new_midterm["traits_to_work_on"], new_midterm["what_you_learned"], new_midterm["proud_of_accomplishment"], new_midterm["is_final"]))

        # Submit Final
        cursor.execute('INSERT INTO reports VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (0, 2, new_final["reporting"], new_final["tid"], new_final["report_for"], new_final["tech_mastery"], new_final["work_ethic"], new_final["communication"], new_final["cooperation"], new_final["initiative"], new_final["team_focus"], new_final["contribution"], new_final["leadership"], new_final["organization"], new_final["delegation"], new_final["points"], new_final["strengths"], new_final["weaknesses"], new_final["traits_to_work_on"], new_final["what_you_learned"], new_final["proud_of_accomplishment"], new_final["is_final"]))

# Send everything to the database
connection.commit()

# Close the connection
connection.close()
