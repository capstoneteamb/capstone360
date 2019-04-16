"""
Note: This db reference needs to be updated to reflect our student/teacher data input/output


Student Table Example
+---------+----------+---------------+----------+---------+-------------------+---------------+
| id      |    tid   |  session_id   |   name   | is_lead |    midterm_done   |   final_done  |
+=========+==========+===============+==========+=========+===================+===============+
| 9228421 |   2315   |      0319     |   Mike   |  false  |       true        |     false     |
+---------+----------+---------------+----------+---------+-------------------+---------------+
"""

from datetime import date
import sqlite3
import datetime
DB_FILE = 'capstone360.db'

class model():
    def __init__(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from capstone_session")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE capstone_session( '
                            'id INTEGER NOT NULL PRIMARY KEY, '
                            'start_term VARCHAR(10) NOT NULL, '
                            'start_year INTEGER NOT NULL, '
                            'end_term VARCHAR(10) NOT NULL, '
                            'end_year INTEGER NOT NULL);')

        try:
            cursor.execute("select count(rowid) from students")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE students( '
                            'id INTEGER NOT NULL, '
                            'tid INTEGER NOT NULL REFERENCES teams(id), '
                            'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                            'name VARCHAR(128) NOT NULL, '
                            'is_lead BOOLEAN NULL DEFAULT FALSE, '
                            'midterm_done BOOLEAN NULL DEFAULT FALSE, '
                            'final_done BOOLEAN NULL DEFAULT FALSE, '
                            'PRIMARY KEY (id, session_id) );')
        try:
            cursor.execute("select count(rowid) from teams")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE teams( '
                            'id INTEGER NOT NULL PRIMARY KEY, '
                            'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                            'name VARCHAR(128) NOT NULL);')

        try:
            cursor.execute("select count(rowid) from team_members")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE team_members( '
                            'tid INTEGER NOT NULL REFERENCES teams(id), '
                            'sid INTEGER NOT NULL REFERENCES students(id), '
                            'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                            'PRIMARY KEY (tid, sid, session_id) );')
        try:
            cursor.execute("select count(rowid) from removed_students")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE removed_students( '
                            'id INTEGER NOT NULL, '
                            'tid INTEGER NOT NULL REFERENCES teams(id), '
                            'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                            'name VARCHAR(128) NOT NULL , '
                            'is_lead BOOLEAN NULL DEFAULT FALSE, '
                            'midterm_done BOOLEAN NULL DEFAULT FALSE, '
                            'final_done BOOLEAN NULL DEFAULT FALSE, '
                            'removed_date DATE, '
                            'PRIMARY KEY (id, session_id) );')
        try:
            cursor.execute("select count(rowid) from team_members")
        except sqlite3.OperationalError:
            cursor.execute('CREATE TABLE team_members( '
                            'tid INTEGER NOT NULL REFERENCES teams(id), '
                            'sid INTEGER NOT NULL REFERENCES students(id), '
                            'session_id INTEGER NOT NULL REFERENCES capstone_session(id), '
                            'PRIMARY KEY (tid, sid, session_id) );')  

        cursor.close()

    def selectStudents(self):

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()

    def getStudents(self, tID, sessionID):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        data = {'tid': tID, 'session_id': sessionID}
        cursor.execute("SELECT name FROM students WHERE tid = :tid AND session_id = :session_id", data)
        return cursor.fetchall()

    def selectTeams(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM teams")
        return cursor.fetchall()

    def getSessionID(self, term, year):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        data = {'start_term': term, 'start_year': year}
        cursor.execute("SELECT * FROM capstone_session WHERE start_term = :start_term AND start_year = :start_year", data)
        return cursor.fetchone()

    def getTeam_sessionID(self, sessionID):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        data = {'session_id': sessionID}
        cursor.execute("SELECT * FROM teams WHERE session_id = :session_id", data)
        return cursor.fetchall()

    def getTeam_ID(self, teamID):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        data = {'id': teamID}
        cursor.execute("SELECT name FROM capstone_session WHERE start_term = :start_term AND start_year = :start_year", data)
        return cursor.fetchone()

    def insertStudent(self, name, id, session_id, tname):
        """
        Insert data into the database
        :param name: String
        :param id: integer
        :param tid: integer
        :param session_id: integer
        """
        params = {'name': tname, 'session_id': session_id}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("select id from teams where name = :name AND session_id = :session_id", params)
        tid = cursor.fetchone()
        tid = tid[0]
        params = {'name': name, 'id': id, 'tid': tid, 'session_id': session_id, 'is_lead': 'false', 'midterm_done': 'false', 'final_done': 'false'}
        cursor = connection.cursor()
        cursor.execute("insert into students (id, tid, session_id, name, is_lead, midterm_done, final_done) VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done, :final_done)", params)
        connection.commit()
        cursor.close()
        return True

    def insertTeam(self, session_id, name):     
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT max(id) FROM teams ")
        result = cursor.fetchone()
        id = result[0]+1
        params = {'id': id, 'session_id': session_id, 'name': name, }
        cursor.execute("insert into teams (id, session_id, name) VALUES (:id, :session_id, :name)", params)
        connection.commit()
        cursor.close()
        return True

    def removeStudent(self, students, session_id):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        for i in students:
            params = {'name':i, 'session_id': session_id}
            cursor.execute("select * from students where name = :name AND session_id = :session_id", params)
            student_infos = cursor.fetchone()
            current_date = datetime.datetime.now()
            date = current_date.strftime("%Y-%m-%d")   
            student_infos = list(student_infos)
            student_infos.append(date)
            cursor.execute("insert into removed_students (id, tid, session_id, name, is_lead, midterm_done, final_done, removed_date) VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done, :final_done, :removed_date)", student_infos)
            cursor.execute("delete from students where name = :name AND session_id = :session_id", params)          
            connection.commit()
        cursor.close()
        return True
    def remove_student_from_team(self, teamID, sessionID):
        connection = sqlite3.connect(DB_FILE)
        data = {'tid': teamID, 'session_id': sessionID}
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE tid = :tid AND session_id = :session_id", data)
        students = cursor.fetchall()
        print(students)
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d")
        for i in students:
            student_infos = list(i)
            student_infos.append(date)
            print(student_infos)
            cursor.execute("insert into removed_students (id, tid, session_id, name, is_lead, midterm_done, final_done, removed_date) VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done, :final_done, :removed_date)", student_infos)
            #cursor.execute("delete from students where tid = :tid", data)  
            connection.commit()
            
        cursor.close()
        return True

    def removeTeam(self, name, session_id):
        
        params = {'name': name, 'session_id': session_id}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("select id from teams where name = :name AND session_id = :session_id", params)
        id = cursor.fetchone()
        id = id[0]
        self.remove_student_from_team(id, session_id)
        params = {'id': id, 'session_id': session_id}
        cursor.execute("delete from students where tid = :id AND session_id = :session_id", params)
        cursor.execute("delete from teams where id = :id AND session_id = :session_id", params)
        connection.commit()
        cursor.close()
        return True
