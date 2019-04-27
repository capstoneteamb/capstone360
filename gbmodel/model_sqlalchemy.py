import os
import sys
sys.path.append(os.getcwd())
from app import db, engine, db_session
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
    def dashboard(self, sessionID):
        student = students()
        session = capstone_session()
        tids = [row[0] for row in self.getTeam_sessionID(sessionID)]
        teamNames = [row[2] for row in self.getTeam_sessionID(sessionID)]
        lists = [[] for _ in range(len(tids))]    
        for i in range(len(tids)):
            names = student.getStudents(tids[i], sessionID)
            temp = [teamNames[i]]
            for name in names:
                temp.append(name[0])
            lists[i] = temp
        sessions = session.getSessions()
        return lists, sessions
        
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
        new_student = students( id = id,tid = tid, session_id = session_id, name = name)       
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
        return True

class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']

    def getMax(self):
        max_id = engine.execute('select max(id) from capstone_session ')
        max_id = max_id.fetchone()
        if max_id[0] is None:
            return 1
        else:
            return max_id[0] + 1
    def insertSession(self, term, year):
        e_term = None
        e_year = 0
        terms = ["Fall", "Winter", "Spring", "Summer"]
        for i in range(len(terms)):
            if terms[i] == term: e_term = terms[(i+1)%4]
        if term == 'Winter': e_year = year+1
        else: e_year = year
        id = self.getMax()
        new_sess = capstone_session(id=id,start_term=term,start_year=year, end_term = e_term, end_year = e_year)
        db.session.add(new_sess)
        db.session.commit()
        return id
            
    def getSessionID(self, term, year):
        id = capstone_session.query.filter(capstone_session.start_term == term, capstone_session.start_year == year).first()    
        if id is None:
            return self.insertSession(term, year)
        else:
            return id.id
    def getSessions(self):
        # lists = engine.execute('select start_term, start_year from capstone_session')
        # lists = lists.fetchall()
        # return lists
        caps = capstone_session.query.all()
        lists = []
        for i in caps:
            temp = str(i.start_term) + " - " + str(i.start_year)
            lists.append(temp)
        return lists

class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    def addStudent(self, s):
        if s is None:
            return False
        s = list(s)
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d") 
        s.append(date)
        engine.execute("insert into removed_students (id, tid, session_id, name, is_lead, midterm_done, final_done, removed_date) VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done, :final_done, :removed_date)", s)
        # removed_student = removed_students(id = s[0], tid = s[1], session_id = s[2],
        #     name = str(s[3]), is_lead = bool(not(s[4])), midterm_done = not(bool(s[5])),final_done=not(bool(s[6])), removed_date = current_date) 
        # db.session.add(removed_student)
        # db.session.commit()
        return True

