import os
import sys
import datetime
from app import db, engine, db_session
from sqlalchemy import exc
from sqlalchemy import update

sys.path.append(os.getcwd())


class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']

    def get_max_team_id(self):
        max_id = engine.execute('select max(id) from teams ')
        max_id = max_id.fetchone()
        if max_id[0] is None:
            return 1
        else:
            return max_id[0] + 1

    def check_dup_team(self, t_name, session_id):
        params = {'name': t_name, 'session_id': session_id}
        result = engine.execute('select * from teams where name = :name and session_id = :session_id', params)
        result = result.fetchone()
        if result is not None:
            return False
        return True

    def insert_team(self, session_id, t_name):
        id = self.get_max_team_id()
        new_team = teams(id=id, session_id=session_id, name=t_name)
        db.session.add(new_team)
        db.session.commit()

    def get_team_session_id(self, session_id):
        result = engine.execute('select * from teams where session_id = :session_id', session_id)
        teams = result.fetchall()
        return teams

    def remove_team(self, name, session_id):
        student = students()
        removed_student = removed_students()
        params = {'name': name, 'session_id': session_id}
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        id = result.fetchone()
        tid = id[0]
        params = {'tid': tid, 'session_id': session_id}
        list_students = student.get_students(tid, session_id)
        print(list_students)
        if list_students is not None:
            for i in list_students:
                params = {'name': i[0], 'session_id': session_id}
                result = engine.execute("select * from students where name = :name AND session_id = :session_id", params)
                s = result.fetchone()
                removed_student.add_student(s)

        params = {'tid': tid, 'session_id': session_id}
        engine.execute("delete from students where tid = :tid AND session_id = :session_id", params)
        engine.execute("delete from teams where id = :tid AND session_id = :session_id", params)
        return True


class students(db.Model):
    __table__ = db.Model.metadata.tables['students']

    def check_dup_student(self, id, session_id):
        params = {'id': id, 'session_id': session_id}
        result = engine.execute('select * from students where id = :id and session_id = :session_id', params)
        result = result.fetchone()
        if result is not None:
            return False
        return True

    def insert_student(self, name, id, session_id, t_name):
        params = {'name': t_name, 'session_id': session_id}
        if not self.check_dup_student(id, session_id):
            return False
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        tid = result.fetchone()
        tid = tid[0]
        new_student = students(id=id, tid=tid, session_id=session_id, name=name, is_lead=0, midterm_done=0, final_done=0)
        db.session.add(new_student)
        db.session.commit()
        return True

    def get_students(self, tid, sessionID):
        data = {'tid': tid, 'session_id': sessionID}
        result = engine.execute('select name from students where tid =:tid and session_id = :session_id', data)
        names = result.fetchall()
        return names

    def update_team(self, member_name, member_tid, member_sessionID):
        update = students.query.filter_by(name=member_name).filter_by(session_id=member_sessionID).update(dict(tid=member_tid))
        db.session.commit()
        return True

    def remove_student(self, sts, t_name, session_id):
        if t_name is None:
            return False
        removed_student = removed_students()
        params = {'name': t_name, 'session_id': session_id}
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id", params)
        id = result.fetchone()
        tid = id[0]
        if sts is None:
            return False
        for i in sts:
            params = {'name': i, 'tid': tid, 'session_id': session_id}
            result = engine.execute("select * from students where name = :name AND tid= :tid AND session_id = :session_id", params)
            s = result.fetchone()
            removed_student.add_student(s)
            data = {'id': s[0], 'session_id': session_id}
            engine.execute('delete from students where id = :id and session_id = :session_id', data)
        return True

    # validate cas username with student id in the database
    def validate(self, id):
        params = {'id': id}
        print(id)
        try:
            result = engine.execute('select session_id from students where name = :id', params)
            result = result.fetchone()
        except exc.SQLAlchemyError:
            result = None
        if result is None:
            return -1
        else:
            result = result[0]
        return result


class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']

    def get_session_id(self, term, year):
        ses_id = capstone_session.query.filter_by(start_term=term, start_year=year).first()
        if (ses_id):
            return ses_id.id
        else:
            return None

    def get_max(self):
        max_id = engine.execute('select max(id) from capstone_session ')
        max_id = max_id.fetchone()
        if max_id[0] is None:
            return 1
        else:
            return max_id[0] + 1

    def insert_session(self, term, year):
        e_term = None
        e_year = 0
        terms = ["Fall", "Winter", "Spring", "Summer"]
        for i in range(len(terms)):
            if terms[i] == term:
                e_term = terms[(i+1) % 4]
        if term == 'Winter':
            e_year = year+1
        else:
            e_year = year
        id = self.get_max()
        new_sess = capstone_session(id=id, start_term=term, start_year=year, end_term=e_term, end_year=e_year)
        db.session.add(new_sess)
        db.session.commit()
        return id

    def getSessionID(self, term, year):
        id = capstone_session.query.filter(capstone_session.start_term == term, capstone_session.start_year == year).first()
        if id is None:
            return self.insert_session(term, year)
        else:
            return id.id

    def get_sessions(self):
        caps = capstone_session.query.all()
        lists = []
        for i in caps:
            temp = str(i.start_term) + " - " + str(i.start_year)
            lists.append(temp)
        return lists


class reports(db.Model):
    __table__ = db.Model.metadata.tables['reports']


class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    def add_student(self, s):
        if s is None:
            return False
        s = list(s)
        del s[7]  # Remove the 'active' attribute. https://docs.python.org/3/tutorial/datastructures.html
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d")
        s.append(date)
        engine.execute("insert into removed_students (id, tid, session_id, name, is_lead, midterm_done, \
            final_done, removed_date) VALUES (:id, :tid, :session_id, :name, :is_lead, \
            :midterm_done, :final_done, :removed_date)", s)
        return True
