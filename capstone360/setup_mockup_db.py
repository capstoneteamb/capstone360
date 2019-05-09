# File: setup-mockup-db.py
# Date: 3/12/2019 (somewhere around there it was first created)
# Description: generates a mockup database with SQLite. Note: information from stack overflow posts were
#              used. I also based some bits of my code off the code on some of the posts and might have
#              transcribed bits from the snippets of the code I saw, but I don't think I did anything that
#              should cause copyright problems)


import sqlite3

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
        "Guy Gregory",
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

# Mock professor data
professors = [("gpld", "George Portland"), ("rdren", "Rick Darren")]

# A model review to base the midterm and final review off of
example_review = {
        "time": 1,
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
        "strengths": ("Everything. You are good at everything. There isn't a "
                      "single problem. Nope."),
        "weaknesses": ("So there are a couple of things. One being your sense"
                       " of humor. Another being your inability and lack of "
                       "willingness to yodel loudly in public places for no "
                       "given reason."),
        "traits_to_work_on": ("Yodeling, Kool-Aid style, wall destroying "
                              "runs, and your decisions to repeatedly press "
                              "the button for the floor you want to go to "
                              "when on the elevator--it doesn't make it go "
                              "faster."),
        "proud_of_accomplishment": "yes?"
}


def generate_student_data():
    id_num = 0
    student_data = []
    for name in names:
        # Generate email address
        split_names = name.split(' ')
        email_address = (
                         # first name
                         split_names[0]

                         + "."

                         # last name
                         + split_names[1]

                         # added to make email address more illegitimate
                         + ".notreal@pdx.edu")

        # Get student id
        student_id = id_num
        id_num = id_num + 1

        # Add Data To List
        student_data.append({"name": name,
                             "email_address": email_address,
                             "id": student_id})

    return student_data


def generate_tables(cursor):
    # Create the professors table
    cursor.execute(('CREATE TABLE professors( '
                    'id VARCHAR(128) NOT NULL PRIMARY KEY, '
                    'name VARCHAR(128) NOT NULL);'))

    # Create capstone session table and insert a row
    cursor.execute(('CREATE TABLE capstone_session( '
                    'id INTEGER NOT NULL PRIMARY KEY, '
                    'start_term VARCHAR(10) NOT NULL, '
                    'start_year INTEGER NOT NULL, '
                    'end_term VARCHAR(10) NOT NULL, '
                    'end_year INTEGER NOT NULL, '
                    'midterm_start DATETIME NULL, '
                    'midterm_end DATETIME NULL, '
                    'final_start DATETIME NULL, '
                    'final_end DATETIME NULL, '
                    'professor_id VARCHAR(128) NOT NULL REFERENCES professors(id));'))

    # Create teams table and insert some rows
    cursor.execute(('CREATE TABLE teams( '
                    'id INTEGER NOT NULL PRIMARY KEY, '
                    'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                    'name VARCHAR(128) NOT NULL);'))

    # Create Students Table
    cursor.execute(('CREATE TABLE students( '
                    'id VARCHAR(128) NOT NULL, '
                    'tid INTEGER NOT NULL REFERENCES teams(id), '
                    'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                    'name VARCHAR(128) NOT NULL, '
                    'is_lead BOOLEAN NOT NULL, '
                    'midterm_done BOOLEAN NOT NULL, '
                    'final_done BOOLEAN NOT NULL, '
                    'active VARCHAR(128) NULL, '
                    'email_address VARCHAR(128) NOT NULL, '
                    'PRIMARY KEY (id, session_id) );'))

    # Create Reports table
    cursor.execute(('CREATE TABLE reports('
                    'time DATETIME NOT NULL, '
                    'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                    'reviewer VARCHAR(128) NOT NULL REFERENCES students(id), '
                    'tid INTEGER NOT NULL REFERENCES teams(id), '
                    'reviewee VARCHAR(128) NOT NULL REFERENCES students(id), '
                    'tech_mastery INTEGER NULL, '
                    'work_ethic INTEGER NULL, '
                    'communication INTEGER NULL, '
                    'cooperation INTEGER NULL, '
                    'initiative INTEGER NULL, '
                    'team_focus INTEGER NULL, '
                    'contribution INTEGER NULL, '
                    'leadership INTEGER NULL, '
                    'organization INTEGER NULL, '
                    'delegation INTEGER NULL, '
                    'points INTEGER NOT NULL, '
                    'strengths VARCHAR(4096) NULL, '
                    'weaknesses VARCHAR(4096) NULL, '
                    'traits_to_work_on VARCHAR(4096) NULL, '
                    'what_you_learned VARCHAR(4096) NULL, '
                    'proud_of_accomplishment VARCHAR(4096) NULL, '
                    'is_final BOOLEAN NOT NULL, '
                    'PRIMARY KEY (reviewer, tid, reviewee, is_final));'))

    # Create removed students table
    cursor.execute(('CREATE TABLE removed_students( '
                    'id VARCHAR(128) NOT NULL, '
                    'tid INTEGER NOT NULL REFERENCES teams(id), '
                    'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                    'name VARCHAR(128) NOT NULL , '
                    'is_lead BOOLEAN NOT NULL, '
                    'midterm_done BOOLEAN NOT NULL, '
                    'final_done BOOLEAN NOT NULL, '
                    'removed_date DATETIME NOT NULL, '
                    'PRIMARY KEY (id, session_id) );'))


def fill_tables_with_data(cursor, student_data, num_sessions, num_teams):
    # Variables that we will need
    start_year = 2019
    end_year = 2019
    start_term_index = 0
    end_term_index = 1
    terms = ["Winter", "Spring", "Summer", "Fall"]

    # Put some entries in the professors table
    for professor in professors:
        cursor.execute('INSERT INTO professors VALUES(?,?)', professor)

    # Put some entries in the capstone_session, students and teams tables
    for session_id in range(num_sessions):
        # Check and, if necessary, reset some variables we use to get our start and end term values
        if (start_term_index > 3):
            start_term_index = 0
            start_year = start_year + 1

        if (end_term_index > 3):
            end_term_index = 0
            end_year = end_year + 1

        # Create a new capstone_session table entry
        cursor.execute(('INSERT INTO capstone_session (id, start_term, start_year, end_term, end_year, '
                        ' professor_id) VALUES(?,?,?,?,?,?)'),
                       (session_id,
                        terms[start_term_index],
                        start_year,
                        terms[end_term_index],
                        end_year,
                        professors[session_id % 2][0]))

        # Increment the variables we use to help us get realistic looking start and end term values
        start_term_index = start_term_index + 1
        end_term_index = end_term_index + 1

        # Create a teams table entry
        for team_id in range(num_teams):
            team_number = team_id + (session_id * num_teams)
            cursor.execute('INSERT INTO teams VALUES(?,?,?)',
                           (team_number,
                            session_id,
                            "Team " + str(team_number)))

        # Create new entries for the students table, using the student_data variable we were given
        for student in student_data:
            # Figure out the student and team ids for the current student
            student_id = student["id"] + (len(student_data) * session_id)
            team_id = student["id"] % num_teams + (num_teams * session_id)

            # Figure out if student is team lead. The will be if they are the first person on the team (the
            # conditional will be true if this is the case)
            is_team_lead = False
            if (student["id"] < num_teams):
                is_team_lead = True

            # Create a students table entry
            cursor.execute('INSERT INTO students VALUES(?,?,?,?,?,?,?,?,?)',
                           (str(student_id),
                            team_id,
                            session_id,
                            student["name"],
                            is_team_lead,
                            False,
                            False,
                            'midterm',
                            student['email_address']))


def run():
    # Part 1: Create database and add tables
    connection = sqlite3.connect('capstone360.db')
    cursor = connection.cursor()
    generate_tables(cursor)

    # Part 2: Add student and student data to database
    fill_tables_with_data(cursor, generate_student_data(), 10, 6)

    # Commit database changes and close the connection to the database
    connection.commit()
    connection.close()


# Run everything only if you are trying to run the script explicitly
# Note: used information from a stack overflow post
if (__name__ == "__main__"):
    run()
