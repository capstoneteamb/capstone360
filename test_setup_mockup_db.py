# File: test_setup-mockup-db.py
# Date: 3/18/2019
# Description: a file to test the mockup database setup script (by seeing if the everything in the database was setup correctly)

import setup_mockup_db, sqlite3

def test_generate_student_data():
    student_data = setup_mockup_db.generate_student_data()
    student_ids = []

    for student in student_data:
        # Check Name
        assert (student["name"] in setup_mockup_db.names)

        # Check that email address is first_name.last_name.pdx.edu
        student_name = student["name"].split(" ")
        assert (len(student_name) == 2)
        assert (student["email_address"] == (student_name[0] + "." + student_name[1] + ".notreal@pdx.edu"))

        # Check that the student id is unique 
        assert (student["id"] not in student_ids)
        student_ids.append(student["id"])

def test_generate_tables():
    # Connect to the database
    connection = sqlite3.connect('mockup-database.db')
    cursor = connection.cursor()

    # Generate the fake database
    setup_mockup_db.generate_tables(cursor)

    # Commit database changes and close the connection to the database
    connection.commit()

    # Check that the database is setup correctly
    
    # Sanity check: the cal to the non-existent table should fail, and we
    # should skip to the except
    try:
        cursor.execute("SELECT * FROM non_existo_tablo;")
        assert (True == False)
    except:
        assert (True)

    # Check that every table we expect to exist exists and check that it has all of the columns we expect
    # Check that the capstone_session table was created, and that it is empty
    cursor.execute("SELECT * FROM capstone_session;")
    assert (not cursor.fetchall())

    # Verify that the columns of the capstone_session table are as we expect
    cursor.execute("PRAGMA table_info(capstone_session);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id" # name
           and columns[0][2] == "INTEGER" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 1 # index in primary key, if it is. 0 if not
    )
    assert(columns[1][1] == "start_term"
           and columns[1][2] == "VARCHAR(10)"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 0
    )
    assert (columns[2][1] == "start_year"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 0
    )
    assert(columns[3][1] == "end_term"
           and columns[3][2] == "VARCHAR(10)"
           and columns[3][3] == 0
           and columns[3][4] == None
           and columns[3][5] == 0
    )
    assert(columns[4][1] == "end_year"
           and columns[4][2] == "INTEGER"
           and columns[4][3] == 0
           and columns[4][4] == None
           and columns[4][5] == 0
    )

    # Verify that the students table was created, and that it is empty
    cursor.execute("SELECT * FROM students;")
    assert (not cursor.fetchall())

    # Verify the columns of the students table
    cursor.execute("PRAGMA table_info(students);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id" # name
           and columns[0][2] == "INTEGER" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 1 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[1][1] == "tid"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 0
    )
    assert (columns[2][1] == "session_id"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 2
    )
    assert(columns[3][1] == "name"
           and columns[3][2] == "VARCHAR(128)"
           and columns[3][3] == 0
           and columns[3][4] == None
           and columns[3][5] == 0
    )
    assert(columns[4][1] == "midterm_done"
           and columns[4][2] == "BOOLEAN"
           and columns[4][3] == 0
           and columns[4][4] == None # False?
           and columns[4][5] == 0
    )
    assert(columns[5][1] == "final_done"
           and columns[5][2] == "BOOLEAN"
           and columns[5][3] == 0
           and columns[5][4] == None # False?
           and columns[5][5] == 0
    )

    # Check that the teams table was created, and that it is empty
    cursor.execute("SELECT * FROM teams;")
    assert (not cursor.fetchall())

    # Now check that the columns of the table are what we expect them to be
    cursor.execute("PRAGMA table_info(teams);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id" # name
           and columns[0][2] == "INTEGER" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 1 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[1][1] == "session_id"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 0
    )
    assert (columns[2][1] == "name"
           and columns[2][2] == "VARCHAR(128)"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 0
    )

    # Check that the team_members table was created, and that it is empty
    cursor.execute("SELECT * FROM team_members;")
    assert (not cursor.fetchall())

    # Now check that the columns of the table are what we expect them to be
    cursor.execute("PRAGMA table_info(team_members);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "tid" # name
           and columns[0][2] == "INTEGER" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 1 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[1][1] == "sid"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 2
    )
    assert (columns[2][1] == "session_id"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 3
    )

    # Check that the table was created and that it is empty
    cursor.execute("SELECT * FROM removed_students;")
    assert (not cursor.fetchall())

    # Now check if the columns are what we expect them to be
    cursor.execute("PRAGMA table_info(removed_students);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "id" # name
           and columns[0][2] == "INTEGER" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 1 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[1][1] == "tid"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 0
    )
    assert (columns[2][1] == "session_id"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 2
    )
    assert(columns[3][1] == "name"
           and columns[3][2] == "VARCHAR(128)"
           and columns[3][3] == 0
           and columns[3][4] == None
           and columns[3][5] == 0
    )
    assert(columns[4][1] == "midterm_done"
           and columns[4][2] == "BOOLEAN"
           and columns[4][3] == 0
           and columns[4][4] == None # False?
           and columns[4][5] == 0
    )
    assert(columns[5][1] == "final_done"
           and columns[5][2] == "BOOLEAN"
           and columns[5][3] == 0
           and columns[5][4] == None # False?
           and columns[5][5] == 0
    )
    assert(columns[6][1] == "session_removed"
           and columns[6][2] == "INTEGER"
           and columns[6][3] == 0
           and columns[6][4] == None
           and columns[6][5] == 0
    )

    # Check if the reports table exists, and that it is empty
    cursor.execute("SELECT * FROM reports;")
    assert (not cursor.fetchall())

    # Check that the colums are what we expect them to be
    cursor.execute("PRAGMA table_info(reports);")
    columns = cursor.fetchall()
    assert(columns[0][1] == "time" # name
           and columns[0][2] == "TIME" # type
           and columns[0][3] == 0 # can be null
           and columns[0][4] == None # default value
           and columns[0][5] == 0 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[1][1] == "session_id"
           and columns[1][2] == "INTEGER"
           and columns[1][3] == 0
           and columns[1][4] == None
           and columns[1][5] == 0
    )
    assert (columns[2][1] == "reporting"
           and columns[2][2] == "INTEGER"
           and columns[2][3] == 0
           and columns[2][4] == None
           and columns[2][5] == 1
    )
    assert(columns[3][1] == "tid"
           and columns[3][2] == "INTEGER"
           and columns[3][3] == 0
           and columns[3][4] == None
           and columns[3][5] == 2
    )
    assert(columns[4][1] == "report_for"
           and columns[4][2] == "INTEGER"
           and columns[4][3] == 0
           and columns[4][4] == None
           and columns[4][5] == 3
    )
    assert(columns[5][1] == "tech_mastery"
           and columns[5][2] == "INTEGER"
           and columns[5][3] == 0 # Should be 1
           and columns[5][4] == None
           and columns[5][5] == 0
    )
    assert(columns[6][1] == "work_ethic"
           and columns[6][2] == "INTEGER"
           and columns[6][3] == 0 # Should be 1
           and columns[6][4] == None
           and columns[6][5] == 0
    )
    assert(columns[7][1] == "communication" # name
           and columns[7][2] == "INTEGER" # type
           and columns[7][3] == 0 # Should be 1
           and columns[7][4] == None # default value
           and columns[7][5] == 0 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[8][1] == "cooperation"
           and columns[8][2] == "INTEGER"
           and columns[8][3] == 0 # Should be 1
           and columns[8][4] == None
           and columns[8][5] == 0
    )
    assert (columns[9][1] == "initiative"
           and columns[9][2] == "INTEGER"
           and columns[9][3] == 0 # Should be 1
           and columns[9][4] == None
           and columns[9][5] == 0
    )
    assert(columns[10][1] == "team_focus"
           and columns[10][2] == "INTEGER"
           and columns[10][3] == 0 # Should be 1
           and columns[10][4] == None
           and columns[10][5] == 0
    )
    assert(columns[11][1] == "contribution"
           and columns[11][2] == "INTEGER"
           and columns[11][3] == 0 # Should be 1
           and columns[11][4] == None
           and columns[11][5] == 0
    )
    assert(columns[12][1] == "leadership"
           and columns[12][2] == "INTEGER"
           and columns[12][3] == 0 # Should be 1... really
           and columns[12][4] == None # False?
           and columns[12][5] == 0
    )
    assert(columns[13][1] == "organization"
           and columns[13][2] == "INTEGER"
           and columns[13][3] == 0 # Should be 1... really
           and columns[13][4] == None
           and columns[13][5] == 0
    )
    assert(columns[14][1] == "delegation" # name
           and columns[14][2] == "INTEGER" # type
           and columns[14][3] == 0 # Should be 1
           and columns[14][4] == None # default value
           and columns[14][5] == 0 # index in primary key, if it is. 0 if not # check if these are right
    )
    assert(columns[15][1] == "points"
           and columns[15][2] == "INTEGER"
           and columns[15][3] == 0
           and columns[15][4] == None
           and columns[15][5] == 0
    )
    assert (columns[16][1] == "strengths"
           and columns[16][2] == "VARCHAR(4096)"
           and columns[16][3] == 0 # Should be 1?
           and columns[16][4] == None
           and columns[16][5] == 0
    )
    assert(columns[17][1] == "weaknesses"
           and columns[17][2] == "VARCHAR(4096)"
           and columns[17][3] == 0 # Should be 1?
           and columns[17][4] == None
           and columns[17][5] == 0
    )
    assert(columns[18][1] == "traits_to_work_on"
           and columns[18][2] == "VARCHAR(4096)"
           and columns[18][3] == 0 # Should be 1?
           and columns[18][4] == None # False?
           and columns[18][5] == 0
    )
    assert(columns[19][1] == "what_you_learned"
           and columns[19][2] == "VARCHAR(4096)"
           and columns[19][3] == 0 # Should be 1?
           and columns[19][4] == None # False?
           and columns[19][5] == 0
    )
    assert(columns[20][1] == "proud_of_accomplishment"
           and columns[20][2] == "VARCHAR(4096)"
           and columns[20][3] == 0 # Should be 1? Maybe?
           and columns[20][4] == None
           and columns[20][5] == 0
    )
    assert(columns[21][1] == "is_final"
           and columns[21][2] == "BOOLEAN"
           and columns[21][3] == 0
           and columns[21][4] == None
           and columns[21][5] == 4
    )

    # Check that the connection is closed
    connection.close()

def test_fill_tables_with_data():
    # Connect to the database
    connection = sqlite3.connect('mockup-database.db')
    cursor = connection.cursor()

    # Get student data
    setup_mockup_db.fill_tables_with_data(cursor, setup_mockup_db.generate_student_data(), 2, 4)
    
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

        # start_term, start_year, end_term, end_year in that order

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
        assert (student[3] in setup_mockup_db.names)

        # Verify that the id is unique for each student entry
        # student[0] = (student) id of the current student
        assert (student[0] not in student_ids)
        student_ids.append(student[0])

        # Verify that the reports have been submitted
        # student[4] = (is) midterm_done (boolean)
        # student[5] = (is) final_done (boolean)
        assert(student[4] and student[5])

    # Verify the data in the team_members table is correct
    # May need to come back and clarify -- the comments are a bit vague
    cursor.execute("SELECT * FROM team_members;")
    team_members = cursor.fetchall()
    for team_member in team_members:
        # Verify that the team id is valid
        # team_member[0] = the team id associated with the given table entry
        assert (team_member[0] in team_ids)

        # Verify that the student id is valid
        # team_member[1] = student id associated with the given table entry
        assert (team_member[1] in student_ids)

        # Verify that the session_id exists
        # team_member[2] = session_id associated with the given table entry
        assert (team_member[2] in session_ids)

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

        # Verify that the "reporting" field contains a valid student id
        # review[2] = the student_id of the one submitting the report
        assert (review[2] in student_ids)

        # Verify that team id is valid
        # review[3] = team_id of the review (the team id of the one being
        # reviewed and the one submitting the review should be the same)
        assert (review[3] in team_ids)

        # Verify that the "report_for" field is valid
        # review[4] = the student id of the student being reviewed
        assert (review[4] in student_ids)

    # Commit database changes and close the connection to the database
    connection.close()

test_generate_student_data()
test_generate_tables()
test_fill_tables_with_data()
