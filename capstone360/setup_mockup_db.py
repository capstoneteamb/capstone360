# File: setup-mockup-db.py
# Date: 3/12/2019 (somewhere around there it was first created)
# Description: generates a mockup database with SQLite. Note: information from stack overflow posts were
#              used. I also based some bits of my code off the code on some of the posts and might have
#              transcribed bits from the snippets of the code I saw, but I don't think I did anything that
#              should cause copyright problems)


import sqlite3
import datetime

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
        student_id = str(id_num)
        id_num = id_num + 1

        # Add Data To List
        student_data.append({"name": name,
                             "email_address": email_address,
                             "id": student_id})

    return student_data


def generate_tables(cursor):
    # Create capstone session table and insert a row
    cursor.execute(('CREATE TABLE capstone_session( '
                    'id INTEGER NOT NULL PRIMARY KEY, '
                    'start_term VARCHAR(10) NOT NULL, '
                    'start_year INTEGER NOT NULL, '
                    'end_term VARCHAR(10) NOT NULL, '
                    'end_year INTEGER NOT NULL );'))

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
                    'is_lead BOOLEAN NOT NULL DEFAULT FALSE, '
                    'midterm_done BOOLEAN NOT NULL DEFAULT FALSE, '
                    'final_done BOOLEAN NOT NULL DEFAULT FALSE, '
                    'active VARCHAR(128) NULL, '
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
                    'is_lead BOOLEAN NOT NULL DEFAULT FALSE, '
                    'midterm_done BOOLEAN NOT NULL DEFAULT FALSE, '
                    'final_done BOOLEAN NOT NULL DEFAULT FALSE, '
                    'active VARCHAR(128) NULL, '
                    'removed_date DATETIME NOT NULL, '
                    'PRIMARY KEY (id, session_id) );'))


def submit_review(cursor, student_id, session_id, review):
    # Put midterm review into database
    cursor.execute(('INSERT INTO reports '
                    'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'),
                   (datetime.datetime.now(),
                    session_id,
                    review["reviewer"],
                    review["tid"],
                    review["reviewee"],
                    review["tech_mastery"],
                    review["work_ethic"],
                    review["communication"],
                    review["cooperation"],
                    review["initiative"],
                    review["team_focus"],
                    review["contribution"],
                    review["leadership"],
                    review["organization"],
                    review["delegation"],
                    review["points"],
                    review["strengths"],
                    review["weaknesses"],
                    review["traits_to_work_on"],
                    review["what_you_learned"],
                    review["proud_of_accomplishment"],
                    review["is_final"]))


def fill_tables_with_data(cursor, student_data, num_sessions, num_teams):
    start_year = 2019
    end_year = 2019
    term_index_start = 0
    term_index_end = 1
    terms = ["Winter", "Spring", "Summer", "Fall"]

    for session_id in range(num_sessions):
        # Get new days and years
        if (term_index_start > 3):
            term_index_start = 0
            start_year = start_year + 1

        if (term_index_end > 3):
            term_index_end = 0
            end_year = end_year + 1

        # Put new session entry into the database
        cursor.execute('INSERT INTO capstone_session VALUES(?,?,?,?,?)',
                       (session_id,
                        terms[term_index_start],
                        start_year,
                        terms[term_index_end],
                        end_year))
        term_index_start = term_index_start + 1
        term_index_end = term_index_end + 1

        # Put new team entry into the database
        for team_id in range(num_teams):
            team_number = team_id + (session_id * num_teams)
            cursor.execute('INSERT INTO teams VALUES(?,?,?)',
                           (team_number,
                            session_id,
                            "Team " + str(team_number)))

        # Put data into the students and teams tables
        for student in student_data:
            student_id = int(student["id"]) + (len(student_data) * session_id)
            team_id = int(student["id"]) % num_teams + (num_teams * session_id)

            # Figure out if student is team lead
            # The conditional will be true if the current student is the first one on the team. If they are
            # the first one, they are the team lead
            is_team_lead = False
            if (int(student["id"]) < num_teams):
                is_team_lead = True

            # Add student to the students table
            cursor.execute('INSERT INTO students VALUES(?,?,?,?,?,?,?,?)',
                           (student_id,
                            team_id,
                            session_id,
                            student["name"],
                            is_team_lead,
                            False,
                            False,
                            'midterm'))


def run():
    # Part 1: Create database and add tables
    connection = sqlite3.connect('mockup_database.db')
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
