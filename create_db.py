import psycopg2


def generate_tables(cursor):

    try:
        # Drops all tables if they exist
        cursor.execute(('DROP TABLE professors, capstone_session, teams, '
                        'students, reports, removed_students cascade;'))

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
                        'midterm_start timestamp NULL, '
                        'midterm_end timestamp NULL, '
                        'final_start timestamp NULL, '
                        'final_end timestamp NULL, '
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
                        'time timestamp NOT NULL, '
                        'session_id INTEGER NOT NULL, '
                        'reviewer VARCHAR(128) NOT NULL, '
                        'tid INTEGER NOT NULL REFERENCES teams(id), '
                        'reviewee VARCHAR(128) NOT NULL, '
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
                        'is_late BOOLEAN NULL, '
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
                        'removed_date timestamp NOT NULL, '
                        'PRIMARY KEY (id, session_id, removed_date));'))
        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table: ", error)


def run():

    # Get db credentials from file
    try:
        db_username = ""
        db_password = ""
        db_name = ""
        with open("/etc/capstone.prod.cfg", "r") as cfg_file:
            for line in cfg_file:
                if "SQLALCHEMY_DATABASE_URI" in line:
                    db_username = line.split('@')[0].split('//')[1].split(':')[0]
                    db_password = line.split('@')[0].split('//')[1].split(':')[1]
                    db_name = line.split('@')[1].split('/')[1][:-2]
    except Exception as error:
        print(error)
        print("Couldn't get database credentials")
        exit()

    # Part 1: Create database and add tables
    connection = psycopg2.connect(user=db_username,
                                  password=db_password,
                                  host="db.cecs.pdx.edu",
                                  port="5432",
                                  database=db_name)
    cursor = connection.cursor()
    generate_tables(cursor)

    # Commit database changes
    connection.commit()

    # Closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


# Run everything only if you are trying to run the script explicitly
if (__name__ == "__main__"):
    run()
