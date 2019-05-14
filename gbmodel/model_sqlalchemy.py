# This file handles the backends from prof_dashboard.py
import os
import sys
import datetime
from app import db, engine, db_session  # noqa
from sqlalchemy import exc, func

sys.path.append(os.getcwd())


class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']

    # Calculate the next id for a newly added team
    # if the table is empty, returns 1
    # Otherwise, return the max id+1
    def get_max_team_id(self):
        try:
            max_id = db.session.query(func.max(teams.id)).scalar()
        except exc.SQLAlchemyError:
            max_id = None
        if max_id is None:
            return 1
        else:
            return max_id + 1

    # Check if the new team name already existed in the given session
    # Input: name of the new team and session id of the selected session
    # Output: return False if the team already exists, True otherwise
    def check_dup_team(self, t_name, session_id):
        try:
            result = teams().query.filter_by(name=t_name, session_id=session_id).first()
        except exc.SQLAlchemyError:
            result = None
        if result is not None:
            return False
        return True

    # Insert a team to database
    # Input: self, session id and name of the new team
    def insert_team(self, session_id, t_name):
        id = self.get_max_team_id()
        new_team = teams(id=id, session_id=session_id, name=t_name)
        db.session.add(new_team)
        db.session.commit()

    # Input: session id of the selected session
    # Output: list of teams and their info. from the selected session
    def get_team_session_id(self, session_id):
        team = teams.query.filter_by(session_id=session_id).all()
        return team

    # Remove a team and all the students from that team
    # Input: name of the team and session id
    def remove_team(self, name, session_id):
        student = students()
        removed_student = removed_students()
        result = teams.query.filter(teams.name == name, teams.session_id == session_id).first()
        tid = result.id
        params = {'tid': tid, 'session_id': session_id}
        list_students = student.get_students(tid, session_id)
        if list_students is not None:
            for i in list_students:
                params = {'name': i, 'session_id': session_id}
                result = engine.execute("select id, tid, session_id, name, is_lead, midterm_done, final_done from students where \
                    name = :name AND session_id = :session_id", params)
                s = result.fetchone()
                removed_student.add_student(s)
        params = {'tid': tid, 'session_id': session_id}
        engine.execute("delete from students where tid = :tid AND session_id = :session_id", params)
        engine.execute("delete from teams where id = :tid AND session_id = :session_id", params)
        return True

    # Return a lists of sessions from the database
    # and a list of teams + students from a selected session
    # Input: session id of the selected session
    def dashboard(self, session_id):
        student = students()
        session = capstone_session()
        tids = [row.id for row in self.get_team_session_id(session_id)]
        team_names = [row.name for row in self.get_team_session_id(session_id)]
        lists = [[] for _ in range(len(tids))]
        for i in range(len(tids)):
            team_members = student.query.filter_by(tid=tids[i], session_id=session_id)
            temp = [team_names[i]]
            for team_member in team_members:
                temp.append({"name": team_member.name, "id": team_member.id})
            lists[i] = temp
        sessions = session.get_sessions()
        return lists, sessions

    def get_team_name_from_id(self, team_id):
        team_name_obj = teams.query.filter_by(id=team_id).first()
        if team_name_obj is not None:
            return team_name_obj.name
        else:
            return None


class students(db.Model):
    __table__ = db.Model.metadata.tables['students']

    # Check if the new added student already exits in the databse
    # Input: id of the student and selected session id
    # Output: return False if the student was already in
    #         return True otherwise
    def check_dup_student(self, id, session_id):
        try:
            result = students.query.filter_by(id=id, session_id=session_id).first()
        except exc.SQLAlchemyError:
            result = None
        if result is not None:
            return False
        return True

    # Add new student
    # Input: student name, student email address, student id, team name and id of the selected session
    # Output: return False if student id already exists in the current session
    #         add student to the database and return True otherwise
    def insert_student(self, name, email_address, id, session_id, t_name):
        result = teams.query.filter(teams.name == t_name, teams.session_id == session_id).first()
        tid = result.id
        new_student = students(id=id,
                               tid=tid,
                               session_id=session_id,
                               name=name,
                               email_address=email_address,
                               is_lead=0,
                               midterm_done=0,
                               final_done=0)
        db.session.add(new_student)
        db.session.commit()
        return True

    def insert_student_no_email(self, name, id, session_id, t_name):
        result = teams.query.filter(teams.name == t_name, teams.session_id == session_id).first()
        tid = result.id
        new_student = students(id=id,
                               tid=tid,
                               session_id=session_id,
                               name=name,
                               is_lead=0,
                               midterm_done=0,
                               final_done=0)
        db.session.add(new_student)
        db.session.commit()
        return True

    # Get a list of students from a team in current session
    # Input: team id, session id
    # Output: list of student name
    def get_students(self, tid, session_id):
        result = [r.name for r in students.query.filter_by(tid=tid, session_id=session_id)]
        return result

    # Remove a list of selected students
    # Input: list of students, team name and session id
    # Output: return False of the list of student is empty
    #         otherwise, remove student from the team
    def remove_student(self, sts, t_name, session_id):
        if t_name is None or sts is None:
            return False
        removed_student = removed_students()
        params = {'name': t_name, 'session_id': session_id}
        result = engine.execute("select id from teams where name = :name AND session_id = :session_id",
                                params)
        id = result.fetchone()
        tid = id[0]

        for i in sts:
            params = {'name': i, 'tid': tid, 'session_id': session_id}
            result = engine.execute("select id, tid, session_id, name, is_lead, midterm_done, final_done from students where name = :name AND tid= :tid AND session_id = :session_id", params)  # noqa
            s = result.fetchone()
            removed_student.add_student(s)
            data = {'id': s[0], 'session_id': session_id}
            engine.execute('delete from students where id = :id and session_id = :session_id', data)
        return True

    # validate cas username with student id in the database
    def validate(self, id):
        params = {'id': id}
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

    # Calculate the next id for a newly added session
    # if the table is empty, returns 1
    # Otherwise, return the max id+1
    def get_max(self):
        max_id = engine.execute('select max(id) from capstone_session ')
        max_id = max_id.fetchone()
        if max_id[0] is None:
            return 1
        else:
            return max_id[0] + 1

    # Add a current session (only if it wasn't in the database)
    # Input: starting term and year of the session
    # Output: return id of the added session
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

    # Get id of a selected session
    # Input: term and year
    # Output: if the term and year are not found, add them to the database and
    #         return added session id. Otherwise, return the id of the session
    def get_session_id(self, term, year):
        try:
            id = capstone_session.query.filter(capstone_session.start_term == term,
                                               capstone_session.start_year == year).first()
        except exc.SQLAlchemyError:
            id = None
        if id is None:
            return self.insert_session(term, year)
        else:
            return id.id

    # Get a list of session to display on the drop downs
    def get_sessions(self):
        caps = capstone_session.query.all()
        lists = []
        for i in caps:
            temp = str(i.start_term) + " - " + str(i.start_year)
            lists.append(temp)
        return lists

    # Check if start and end dates are valid
    # Input: start and end dates
    # Output: Return 0 if valid, return 1 if start date is after the end date
    #         Return 1 if either start or end date is empty
    def check_dates(self, start, end):
        params = {'start': start, 'end': end}
        if params['start'] and params['end']:
            if int(params['start']) > int(params['end']):
                return 1
            else:
                return 0
        elif params['start'] is None and params['end'] is None:
            return 0
        return 2

    # Display msg error for inserting dates
    def date_error(self, params):
        error_msg = None
        for i in params:
            if params[i]:
                params[i] = params[i].replace('-', '')
            else:
                params[i] = None
        mid = self.check_dates(params['midterm_start'], params['midterm_end'])
        final = self.check_dates(params['final_start'], params['final_end'])
        if mid == 2:
            error_msg = "Please fill out both start and end dates for the Midterm dates"
            return error_msg
        if final == 2:
            error_msg = "Please fill out both start and end dates for the Final dates"
            return error_msg
        elif mid == 1 or final == 1:
            error_msg = "Please choose an end date that starts after the start date"
            return error_msg
        return error_msg

    # Split dates into integer year, month and day
    # to convert the string to datetime object
    def split_dates(self, params):
        for i in params:
            if params[i]:
                params[i] = params[i].split('-')
                params[i] = datetime.datetime(int(params[i][0]), int(params[i][1]), int(params[i][2]))
            else:
                params[i] = None
        return params

    # Insert a start and end date for midterm and final review
    # Input: start and end date for midterm review and final reviews
    # Output: update the dates in the database
    def insert_dates(self, midterm_start, midterm_end, final_start, final_end, session_id):
        review_dates = {'midterm_start': midterm_start,
                        'midterm_end': midterm_end,
                        'final_start': final_start,
                        'final_end': final_end}
        dates = self.split_dates(review_dates)
        params = {'midterm_start': dates['midterm_start'],
                  'midterm_end': dates['midterm_end'],
                  'final_start': dates['final_start'],
                  'final_end': dates['final_end'],
                  'session_id': session_id}
        for i in params:
            if params[i]:
                params[i] = params[i]
            else:
                params[i] = None
        session = capstone_session.query.filter(capstone_session.id == session_id).first()
        session.midterm_start = params['midterm_start']
        session.midterm_end = params['midterm_end']
        session.final_start = params['final_start']
        session.final_end = params['final_end']
        db.session.commit()
        return True


class reports(db.Model):
    __table__ = db.Model.metadata.tables['reports']

    def get_reports_for_student(self, student_id, term_id, is_final=None):
        """
        Gets all available reports for a student, optionally filtering to only midterms or finals.
        """
        if is_final is not None:
            query_string = "select * from reports where reviewee=:id and tid=:term_id and is_final=:is_final"
        else:
            query_string = "select * from reports where reviewee=:id and tid=:term_id"

        params = {'id': student_id, 'term_id': term_id, 'is_final': is_final}
        reports = engine.execute(query_string, params)

        return reports

    def check_report_submitted(self, team_id, reviewing_student_id, reviewee_student_id, is_final):
        params = {"reviewer": reviewing_student_id,
                  "reviewee": reviewee_student_id,
                  "tid": team_id,
                  "is_final": is_final}
        results = engine.execute(("select time from reports where "
                                  "reporting = :reviewer "
                                  "AND report_for = :reviewee "
                                  "AND tid = :tid AND "
                                  "is_final = :is_final ;"), params)
        return results.fetchone() is not None

    def get_report(self, reviewer_id, reviewee_id, tid, is_final):
        params = {"reviewer": reviewer_id, "reviewee": reviewee_id, "tid": tid, "is_final": is_final}
        result = engine.execute(("select * from reports where reporting = :reviewer AND tid = :tid"
                                 " AND report_for = :reviewee AND is_final = :is_final"), params)
        print(params)
        return result.fetchone()


class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    # Insert removed students into remocved_students table
    # Input: student info
    # Output: return False if the info is empty
    #         Otherwise, add student to the list and return True
    def add_student(self, s):
        if s is None:
            return False
        s = list(s)
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d")
        s.append(date)
        engine.execute("insert into removed_students (id, tid, session_id, \
            name, is_lead, midterm_done, final_done, removed_date) \
                VALUES (:id, :tid, :session_id, :name, :is_lead, :midterm_done,\
                     :final_done, :removed_date)", s)
        return True
