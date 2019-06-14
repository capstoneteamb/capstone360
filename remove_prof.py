import psycopg2

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

# Get the professor id of the professor we want to remove
id = input("Please enter a professor id: ")

# Try to remove the professor to the db
try:
    connection = psycopg2.connect(user=db_name,
                                  password=db_password,
                                  host="db.cecs.pdx.edu",
                                  port="5432",
                                  database=db_name)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PROFESSORS WHERE id = %s", (id))
    connection.commit()
    print("Professor removed.")
except Exception as error:
    if(connection):
        print("Failed to remove professor")
    print(error)
finally:
    if(connection):
        cursor.close()
        connection.close()
