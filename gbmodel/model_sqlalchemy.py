import os
import sys
#sys.path.append('/Users/faisa/Desktop/Code/capstone_repo/capstone360')
from app import db, engine
import datetime

class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']

    def getMaxTeamID(self):
        max_id = engine.execute('select max(id) from teams ')
        max_id = max_id.fetchone()
        if max_id[0] is None:
            return 1
        else:
            return max_id[0] + 1
            
    def checkDupTeam(self, tName, sessionID):
        params = {'name': tName, 'session_id': sessionID}
        result = engine.execute('select * from teams where name = :name and session_id = :session_id', params)
        result = result.fetchone()
        if result is not None:
            return False
        return True

    def insertTeam(self, session_id, tName):
        id = self.getMaxTeamID()
        new_team = teams(id=id,session_id=session_id,name=tName)
        db.session.add(new_team)
        db.session.commit()

    def getTeam_sessionID(self, session_id):
        result = engine.execute('select * from teams where session_id = :session_id', session_id)
        teams = result.fetchall()
        return teams

    def removeTeam(self, name, session_id):
        student = students()
        removed_student = removed_students()
        params = {'name': name, 'session_id': session_id}
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        id = result.fetchone()
        tid = id[0]
        params = {'tid':tid, 'session_id':session_id}
        list_students = student.getStudents(tid, session_id)
        print(list_students)
        if list_students is not None:      
            for i in list_students:
                params = {'name':i[0], 'session_id': session_id}
                result = engine.execute("select * from students where name = :name AND session_id = :session_id", params)
                s = result.fetchone()
                removed_student.addStudent(s)
              
        params = {'tid': tid, 'session_id': session_id}
        engine.execute("delete from students where tid = :tid AND session_id = :session_id", params)
        engine.execute("delete from teams where id = :tid AND session_id = :session_id", params)
        return True

class students(db.Model):
    __table__ = db.Model.metadata.tables['students']

    def checkDupStudent(self, id, session_id):
        params = {'id': id, 'session_id': session_id}
        result = engine.execute('select * from students where id = :id and session_id = :session_id', params)
        result = result.fetchone()
        if result is not None:
            return False
        return True

    def insertStudent(self, name, id, session_id, tname):
        params = {'name': tname, 'session_id': session_id}
        if not self.checkDupStudent(id, session_id):
            return False
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        tid = result.fetchone()
        tid = tid[0]
        new_student = students(id = id, tid = tid, session_id = session_id, name = name, is_lead = 0, midterm_done = 0, final_done = 0)
        db.session.add(new_student)
        db.session.commit()
        return True
    
    def getStudents(self, tid, sessionID):
        data = {'tid': tid, 'session_id': sessionID}
        result = engine.execute('select name from students where tid =:tid and session_id = :session_id', data)
        names = result.fetchall()
        return names

    def removeStudent(self, sts, tName, session_id):
        if tName is None:
            return False
        removed_student = removed_students()
        params = {'name': tName, 'session_id': session_id}
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        id = result.fetchone()
        tid = id[0] 
        if sts is None:
            return False       
        for i in sts:
            params = {'name':i, 'tid':tid, 'session_id': session_id}
            result = engine.execute("select * from students where name = :name AND tid= :tid AND session_id = :session_id", params)
            s = result.fetchone()
            removed_student.addStudent(s)
            # students.delete().where(students.id == s[3], students.session_id == session_id) 
            data = {'id':s[0], 'session_id': session_id}
            engine.execute('delete from students where id = :id and session_id = :session_id', data)
            # consider another statement to remove the student entry from the team_members table
        return True

class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']

    def getSessionID(self, term, year):
        #id = capstone_session.query.filter(capstone_session.start_term == term, capstone_session.start_year == year).first()    
        ses_id = capstone_session.query.filter_by(start_term = term, start_year = year).first()
        if (ses_id):
            return ses_id.id
        else:
            return None
class team_members(db.Model):
    __table__ = db.Model.metadata.tables['team_members']

class reports(db.Model):
    __table__ = db.Model.metadata.tables['reports']

class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    def addStudent(self, s):
        if s is None:
            return False
        s = list(s)
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d") 
        s.append(date)
        engine.execute("insert into removed_students (id, tid, session_id, name, is_lead, midterm_done, final_done, active, removed_date) VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done, :final_done, :active, :removed_date)", s)
        # removed_student = removed_students(id = s[0], tid = s[1], session_id = s[2],
        #     name = str(s[3]), is_lead = bool(not(s[4])), midterm_done = not(bool(s[5])),final_done=not(bool(s[6])), removed_date = current_date) 
        # db.session.add(removed_student)
        # db.session.commit()
        return True
