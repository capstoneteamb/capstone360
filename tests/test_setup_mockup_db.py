# File: test_setup-mockup-db.py
# Date: 3/18/2019
# Description: a file to test the mockup database setup script (by seeing if the everything in the database
#              was setup correctly). Note: information from stack overflow posts were used. I also based
#              some bits of my code off the code on some of the posts and might have transcribed snippets of
#              some of the code I saw (from the posts), but I don't think I did anything that should
#              cause copyright problems)

from capstone360.setup_mockup_db import names, generate_student_data, generate_tables, fill_tables_with_data
import sqlite3
import os
from cryptography.fernet import Fernet
key_file = open("key.txt")
key = key_file.readline()
key = bytes(key.encode("UTF8"))
cipher = Fernet(key)


def encrypt(p_text):
    c_text = cipher.encrypt(bytes(p_text, encoding='UTF8'))  # Encrypt name
    return c_text


def decrypt(c_text):
    p_text = cipher.decrypt(c_text)
    p_text = p_text.decode('UTF8')
    return p_text

# Global Variables
mockup_db_path = "temp_database.db"


def test_generate_student_data():
    student_data = generate_student_data()
    student_ids = []

    for student in student_data:
        # Check Name
        assert (decrypt(student["name"]) in names)

        # Check that email address is first_name.last_name.pdx.edu
        student_name = student["name"].split(" ")
        assert (len(student_name) == 2)
        assert (student["email_address"]
                == (student_name[0]
                + "."
                + student_name[1]
                + ".notreal@pdx.edu"))

        # Check that the student id is unique
        assert (student["id"] not in student_ids)
        student_ids.append(student["id"])


def test_generate_tables():
    # Connect to the database
    connection = sqlite3.connect(mockup_db_path)
    cursor = connection.cursor()

    # Generate the fake database
    generate_tables(cursor)

    # Commit database changes and close the connection to the database
    connection.commit()

    # Sanity check: the cal to the non-existent table should fail, and we
    # should skip to the except
    try:
        cursor.execute("SELECT * FROM non_existo_tablo;")
        assert (True is False)
    except sqlite3.OperationalError:
        assert (True)

    # Check that the professors table was created, and that it is empty
    cursor.execute("SELECT * FROM professors;")
    assert (not cursor.fetchall())

    # Verify that the columns of the professors table are as we expect
    cursor.execute("PRAGMA table_info(professors);")
    columns = cursor.fetchall()
    assert(
        # db column name
        columns[0][1] == "id"
        # db column type
        and columns[0][2] == "VARCHAR(128)"
        # if the value in this column can be null
        # - 1 = NOT NULL
        # - 0 = NULL
        and columns[0][3] == 1
        # the default value for this db column
        and columns[0][4] is None
        # the index of the column in the primary key, if it is a part of it (I think). 0 otherwise
        and columns[0][5] == 1)
    assert(columns[1][1] == "name"
           and columns[1][2] == "VARCHAR(128)"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)

    # Check that the capstone_session table was created, and that it is empty
    cursor.execute("SELECT * FROM capstone_session;")
    assert (not cursor.fetchall())

    # Verify that the columns of the capstone_session table are as we expect
    cursor.execute("PRAGMA table_info(capstone_session);")
    columns = cursor.fetchall()
    assert(
        columns[0][1] == "id"
        and columns[0][2] == "INTEGER"
        and columns[0][3] == 1
        and columns[0][4] is None
        and columns[0][5] == 1)
    assert(columns[1][1] == "start_term"
           and columns[1][2] == "VARCHAR(10)"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)
    assert(columns[2][1] == "start_year"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 1
           and columns[2][4] is None
           and columns[2][5] == 0)
    assert(columns[3][1] == "end_term"
           and columns[3][2] == "VARCHAR(10)"
           and columns[3][3] == 1
           and columns[3][4] is None
           and columns[3][5] == 0)
    assert(columns[4][1] == "end_year"
           and columns[4][2] == "INTEGER"
           and columns[4][3] == 1
           and columns[4][4] is None
           and columns[4][5] == 0)
    assert(columns[5][1] == "midterm_start"
           and columns[5][2] == "DATETIME"
           and columns[5][3] == 0
           and columns[5][4] is None
           and columns[5][5] == 0)
    assert(columns[6][1] == "midterm_end"
           and columns[6][2] == "DATETIME"
           and columns[6][3] == 0
           and columns[6][4] is None
           and columns[6][5] == 0)
    assert(columns[7][1] == "final_start"
           and columns[7][2] == "DATETIME"
           and columns[7][3] == 0
           and columns[7][4] is None
           and columns[7][5] == 0)
    assert(columns[8][1] == "final_end"
           and columns[8][2] == "DATETIME"
           and columns[8][3] == 0
           and columns[8][4] is None
           and columns[8][5] == 0)
    assert(columns[9][1] == "professor_id"
           and columns[9][2] == "VARCHAR(128)"
           and columns[9][3] == 1
           and columns[9][4] is None
           and columns[9][5] == 0)

    # Verify that the students table was created, and that it is empty
    cursor.execute("SELECT * FROM students;")
    assert (not cursor.fetchall())

    # Verify the columns of the students table
    cursor.execute("PRAGMA table_info(students);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id"
           and columns[0][2] == "VARCHAR(128)"
           and columns[0][3] == 1
           and columns[0][4] is None
           and columns[0][5] == 1)
    assert(columns[1][1] == "tid"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)
    assert(columns[2][1] == "session_id"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 1
           and columns[2][4] is None
           and columns[2][5] == 2)
    assert(columns[3][1] == "name"
           and columns[3][2] == "VARCHAR(128)"
           and columns[3][3] == 1
           and columns[3][4] is None
           and columns[3][5] == 0)
    assert(columns[4][1] == "is_lead"
           and columns[4][2] == "BOOLEAN"
           and columns[4][3] == 1
           and columns[4][4] is None
           and columns[4][5] == 0)
    assert(columns[5][1] == "midterm_done"
           and columns[5][2] == "BOOLEAN"
           and columns[5][3] == 1
           and columns[5][4] is None
           and columns[5][5] == 0)
    assert(columns[6][1] == "final_done"
           and columns[6][2] == "BOOLEAN"
           and columns[6][3] == 1
           and columns[6][4] is None
           and columns[6][5] == 0)
    assert(columns[7][1] == "active"
           and columns[7][2] == "VARCHAR(128)"
           and columns[7][3] == 0
           and columns[7][4] is None
           and columns[7][5] == 0)
    assert(columns[8][1] == "email_address"
           and columns[8][2] == "VARCHAR(128)"
           and columns[8][3] == 1
           and columns[8][4] is None
           and columns[8][5] == 0)

    # Check that the teams table was created, and that it is empty
    cursor.execute("SELECT * FROM teams;")
    assert (not cursor.fetchall())

    # Now check that the columns of the table are what we expect them to be
    cursor.execute("PRAGMA table_info(teams);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id"
           and columns[0][2] == "INTEGER"
           and columns[0][3] == 1
           and columns[0][4] is None
           and columns[0][5] == 1)
    assert(columns[1][1] == "session_id"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)
    assert(columns[2][1] == "name"
           and columns[2][2] == "VARCHAR(128)"
           and columns[2][3] == 1
           and columns[2][4] is None
           and columns[2][5] == 0)

    # Check that the table was created and that it is empty
    cursor.execute("SELECT * FROM removed_students;")
    assert (not cursor.fetchall())

    # Now check if the columns are what we expect them to be
    cursor.execute("PRAGMA table_info(removed_students);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id"
           and columns[0][2] == "VARCHAR(128)"
           and columns[0][3] == 1
           and columns[0][4] is None
           and columns[0][5] == 1)
    assert(columns[1][1] == "tid"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)
    assert(columns[2][1] == "session_id"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 1
           and columns[2][4] is None
           and columns[2][5] == 2)
    assert(columns[3][1] == "name"
           and columns[3][2] == "VARCHAR(128)"
           and columns[3][3] == 1
           and columns[3][4] is None
           and columns[3][5] == 0)
    assert(columns[4][1] == "is_lead"
           and columns[4][2] == "BOOLEAN"
           and columns[4][3] == 1
           and columns[4][4] is None
           and columns[4][5] == 0)
    assert(columns[5][1] == "midterm_done"
           and columns[5][2] == "BOOLEAN"
           and columns[5][3] == 1
           and columns[5][4] is None
           and columns[5][5] == 0)
    assert(columns[6][1] == "final_done"
           and columns[6][2] == "BOOLEAN"
           and columns[6][3] == 1
           and columns[6][4] is None
           and columns[6][5] == 0)
    assert(columns[7][1] == "removed_date"
           and columns[7][2] == "DATETIME"
           and columns[7][3] == 1
           and columns[7][4] is None
           and columns[7][5] == 0)

    # Check if the reports table exists, and that it is empty
    cursor.execute("SELECT * FROM reports;")
    assert (not cursor.fetchall())

    # Check that the colums are what we expect them to be
    cursor.execute("PRAGMA table_info(reports);")
    columns = cursor.fetchall()
    assert(
           # name
           columns[0][1] == "time"
           # data type
           and columns[0][2] == "DATETIME"
           # can be null
           #  - 1 = NOT NULL
           #  - 0 = NULL
           and columns[0][3] == 1
           # the default value
           and columns[0][4] is None
           # index in the primary key, if it is one. If not, it is 0. # check if these are right
           and columns[0][5] == 0)
    assert(columns[1][1] == "session_id"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 1
           and columns[1][4] is None
           and columns[1][5] == 0)
    assert(columns[2][1] == "reviewer"
           and columns[2][2] == "VARCHAR(128)"
           and columns[2][3] == 1
           and columns[2][4] is None
           and columns[2][5] == 1)
    assert(columns[3][1] == "tid"
           and columns[3][2] == "INTEGER"
           and columns[3][3] == 1
           and columns[3][4] is None
           and columns[3][5] == 2)
    assert(columns[4][1] == "reviewee"
           and columns[4][2] == "VARCHAR(128)"
           and columns[4][3] == 1
           and columns[4][4] is None
           and columns[4][5] == 3)
    assert(columns[5][1] == "tech_mastery"
           and columns[5][2] == "INTEGER"
           and columns[5][3] == 0
           and columns[5][4] is None
           and columns[5][5] == 0)
    assert(columns[6][1] == "work_ethic"
           and columns[6][2] == "INTEGER"
           and columns[6][3] == 0
           and columns[6][4] is None
           and columns[6][5] == 0)
    assert(columns[7][1] == "communication"
           and columns[7][2] == "INTEGER"
           and columns[7][3] == 0
           and columns[7][4] is None
           and columns[7][5] == 0)
    assert(columns[8][1] == "cooperation"
           and columns[8][2] == "INTEGER"
           and columns[8][3] == 0
           and columns[8][4] is None
           and columns[8][5] == 0)
    assert(columns[9][1] == "initiative"
           and columns[9][2] == "INTEGER"
           and columns[9][3] == 0
           and columns[9][4] is None
           and columns[9][5] == 0)
    assert(columns[10][1] == "team_focus"
           and columns[10][2] == "INTEGER"
           and columns[10][3] == 0
           and columns[10][4] is None
           and columns[10][5] == 0)
    assert(columns[11][1] == "contribution"
           and columns[11][2] == "INTEGER"
           and columns[11][3] == 0
           and columns[11][4] is None
           and columns[11][5] == 0)
    assert(columns[12][1] == "leadership"
           and columns[12][2] == "INTEGER"
           and columns[12][3] == 0
           and columns[12][4] is None
           and columns[12][5] == 0)
    assert(columns[13][1] == "organization"
           and columns[13][2] == "INTEGER"
           and columns[13][3] == 0
           and columns[13][4] is None
           and columns[13][5] == 0)
    assert(columns[14][1] == "delegation"
           and columns[14][2] == "INTEGER"
           and columns[14][3] == 0
           and columns[14][4] is None
           and columns[14][5] == 0)
    assert(columns[15][1] == "points"
           and columns[15][2] == "INTEGER"
           and columns[15][3] == 1
           and columns[15][4] is None
           and columns[15][5] == 0)
    assert(columns[16][1] == "strengths"
           and columns[16][2] == "VARCHAR(4096)"
           and columns[16][3] == 0
           and columns[16][4] is None
           and columns[16][5] == 0)
    assert(columns[17][1] == "weaknesses"
           and columns[17][2] == "VARCHAR(4096)"
           and columns[17][3] == 0
           and columns[17][4] is None
           and columns[17][5] == 0)
    assert(columns[18][1] == "traits_to_work_on"
           and columns[18][2] == "VARCHAR(4096)"
           and columns[18][3] == 0
           and columns[18][4] is None
           and columns[18][5] == 0)
    assert(columns[19][1] == "what_you_learned"
           and columns[19][2] == "VARCHAR(4096)"
           and columns[19][3] == 0
           and columns[19][4] is None
           and columns[19][5] == 0)
    assert(columns[20][1] == "proud_of_accomplishment"
           and columns[20][2] == "VARCHAR(4096)"
           and columns[20][3] == 0
           and columns[20][4] is None
           and columns[20][5] == 0)
    assert(columns[21][1] == "is_final"
           and columns[21][2] == "BOOLEAN"
           and columns[21][3] == 1
           and columns[21][4] is None
           and columns[21][5] == 4)

    # Check that the connection is closed
    connection.close()


def test_fill_tables_with_data():
    # Connect to the database
    connection = sqlite3.connect(mockup_db_path)
    cursor = connection.cursor()

    # Get student data
    fill_tables_with_data(cursor, generate_student_data(), 2, 4)

    # Verify that the data in the professors table is correct
    cursor.execute("SELECT * FROM professors;")
    professors = cursor.fetchall()
    professor_ids = []
    for professor in professors:
        # Vefify that the professor id is unique
        assert (professor[0] not in professor_ids)
        professor_ids.append(professor[0])

    # Verify that the data in the session table is correct
    cursor.execute("SELECT * FROM capstone_session;")
    sessions = cursor.fetchall()
    session_ids = []
    assert (len(sessions) == 2)
    for session in sessions:
        # Verify that the session id is unique
        # session[0] = (session) id of the current session
        assert (session[0] not in session_ids)
        session_ids.append(session[0])

        # Verify that professor id is in the professors table
        assert(session[9] in professor_ids)

    # Verify that the data in the teams table is correct
    cursor.execute("SELECT * FROM teams;")
    teams = cursor.fetchall()
    team_ids = []
    for team in teams:
        # Verify that the team is associated with a capstone session id
        # team[1] = session id associated with the current team
        assert (team[1] in session_ids)

        # Verify that the team id is unique
        # team[0] = the (team) id associated with the current team
        assert (team[0] not in team_ids)
        team_ids.append(team[0])

        # Verify that we have team names -- not sure if this is correct
        # team[2] = the name of the team
        assert (team[2])

    # Check that each student has been added to the student's table
    cursor.execute("SELECT * FROM students;")
    students = cursor.fetchall()
    student_ids = []
    for student in students:
        # Verify that the name of the student is the names database
        # student[3] = name of the student
        assert (student[3] in names)

        # Verify that the id is unique for each student entry
        # student[0] = (student) id of the current student
        assert (student[0] not in student_ids)
        student_ids.append(student[0])

    # Verify the data in the reports table is correct
    # Might want to change comments here as well
    cursor.execute("SELECT * FROM reports;")
    reviews = cursor.fetchall()
    for review in reviews:
        # Verify that the time field is non-empty
        # review[0] = time report was submitted
        assert (review[0])

        # Verify that the session id is valid
        # review[1] = session id associated with the report
        assert (review[1] in session_ids)

        # Verify that the "reviewer" field contains a valid student id
        # review[2] = the student_id of the one submitting the report
        assert (review[2] in student_ids)

        # Verify that team id is valid
        # review[3] = team_id of the review (the team id of the one being
        # reviewed and the one submitting the review should be the same)
        assert (review[3] in team_ids)

        # Verify that the "reviewee" field is valid
        # review[4] = the student id of the student being reviewed
        assert (review[4] in student_ids)

    # Commit database changes and close the connection to the database
    connection.close()

    # Remove the mockup db file (this might get in the way of testing
    # Note: used information from a stack overflow post to write this
    os.remove(mockup_db_path)
