import os
import sys
import datetime
import logging
import traceback
from extensions import db
from sqlalchemy import exc, func

sys.path.append(os.getcwd())


def log_exception():
    exception_details = sys.exc_info()
    error = "Gbmodel - {}: {}".format(exception_details[0].__name__, exception_details[1])
    logging.error(error)
    traceback.print_tb(exception_details[2])


class professors(db.Model):
    """
    Class for the professors table
    Table column data imported automatically
    """
    __table__ = db.Model.metadata.tables['professors']

    def get_professor(self, id):
        """
        Get a professor with the given id
        Input: professor id
        Output: the professor object associated with the given id
        """
        try:
            result = professors.query.filter(professors.id == id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None

        if result is None:
            return False
        return result

    def get_all_professors(self):
        """
        Get a list of all professors in the database (by id)
        Input: none
        Output: a list of professors
        """
        try:
            profs = professors().query.all()
            lists = []
            for i in profs:
                temp = i
                lists.append(temp)
        except exc.SQLAlchemyError:
            log_exception()
            profs = None

        if profs is None:
            return False
        return lists

    def check_professor(self, prof_id):
        """
        Checks if professor ID exists in the DB
        Input: professor ID given
        Output: True if it exists, False otherwise
        """
        try:
            prof_id = prof_id.strip().lower()
            result = professors().query.filter_by(id=prof_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None

        if result is not None:
            return True
        return False

    def prof_id(self, name):
        """
        Gets the id of the professor with the given name, if he is found. Returns -1 otherwise
        Input: professor name
        Output: return professor's id
        """
        try:
            prof = professors.query.filter_by(name=name).first()
        except exc.SQLAlchemyError:
            log_exception()
            prof = None

        if prof is None:
            return -1
        return prof.id


class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']

    def get_max_team_id(self):
        """
        Calculate the next id for a newly added team
        if the table is empty, returns 1
        Otherwise, return the max id+1
        """
        try:
            max_id = db.session.query(func.max(teams.id)).scalar()
        except exc.SQLAlchemyError:
            log_exception()
            max_id = None

        if max_id is None:
            return 1
        else:
            return max_id + 1

    def check_dup_team(self, t_name, session_id):
        """
        Check if the new team name already existed in the given session
        Input: name of the new team and session id of the selected session
        Output: return False if the team already exists, True otherwise
        """
        try:
            result = teams().query.filter_by(name=t_name,
                                             session_id=session_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None

        if result is not None:
            return False
        return True

    def insert_team(self, session_id, t_name):
        """
        Insert a team to database
        Input: self, session id and name of the new team
        """
        id = self.get_max_team_id()
        new_team = teams(id=id, session_id=session_id, name=t_name)
        db.session.add(new_team)
        db.session.commit()
        return id

    def get_team_session_id(self, session_id):
        """
        Get a list of all of the teams in a session
        Input: session id of the selected session
        Output: list of teams and their info from the selected session
        """
        try:
            if session_id:
               team = teams.query.filter_by(session_id=session_id).all()

               if team is None:
                   return []
               return team
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def remove_team_from_session(self, name, session_id):
        """
        Remove a team and all the students from that team
        Input: name of the team and session id
        Output: True if the operation completed successfully. False if something went wrong
        """
        try:
            student = students()
            removed_student = removed_students()
            result = teams.query.filter(teams.name == name,
                                        teams.session_id == session_id).first()
            tid = result.id
            list_students = student.get_students(tid)
            if list_students is not None:
                for i in list_students:
                    result = students.query.filter(students.name == i,
                                                   students.session_id == session_id).first()
                    removed_student.add_student(result)
            student_list = students.query.filter(students.tid == tid,
                                                 students.session_id == session_id).all()
            for i in student_list:
                db.session.delete(i)
                db.session.commit()
            team = teams.query.filter(teams.id == tid, teams.session_id == session_id).first()
            db.session.delete(team)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            return False

    def remove_team(self, name, session_id):
        """
        Remove a team and all the students from that team
        Input: name of the team and session id
        Output: delete a team
                move all student in the team to unassigned student
        """
        try:
            # Get the team slated for removal
            teams_obj = teams()
            team = teams_obj.query.filter(teams.name == name,
                                          teams.session_id == session_id).first()

            # Get the students on the team
            student_list = students.query.filter(students.tid == team.id,
                                                 students.session_id == session_id).all()

            # If we are trying to remove a team with students on it...
            if student_list:
                # Jump ship if the team is the empty team. We don't delete the empty team if there are
                # students in it
                if name == "":
                    return False

                # Otherwise, move all the students on the team to the empty team
                empty_team_id = teams_obj.get_tid_from_name("", session_id)
                if empty_team_id is None:
                    empty_team_id = teams_obj.insert_team(session_id, "")
                for student in student_list:
                    student.midterm_done = False
                    student.final_done = False
                    student.tid = empty_team_id

            # Remove all of the review submitted with team id
            reviews = reports.query.filter(reports.tid == team.id).all()
            for review in reviews:
                db.session.delete(review)

            # Now, remove the team
            db.session.delete(team)

            # Commit db changes
            db.session.commit()

            # Indicate operation successful
            return True
        except exc.SQLAlchemyError:
            # Log exception, and rollback db changes
            log_exception()
            db.session.rollback()
            return False

    def dashboard(self, session_id):
        """
        Return a lists of sessions from the database
        and a list of teams + students from a selected session
        Input: session id of the selected session
        """
        student = students()
        session = capstone_session()
        today = datetime.datetime.now()
        teams = self.get_team_session_id(session_id)
       
        tids = []
        team_names = []
        if teams is not None:
            for row in teams:
                if row is not None:
                    tids.append(row.id)
                    team_names.append(row.name)
        lists = [[] for _ in range(len(tids))]
        flag = 0
        for i in range(len(tids)):
            # Get min and max
            try:
                # Query to get the min & max student points of their final
                final_points = db.session.query(
                    func.max(reports.points).label("max_points"),
                    func.min(reports.points).label("min_points"),
                    reports.reviewee).filter_by(tid=tids[i], is_final=True).filter(
                        reports.reviewee != reports.reviewer).group_by(reports.reviewee)
                # Query to get the min & max student points of their midterm
                midterm_points = db.session.query(
                    func.max(reports.points).label("max_points"),
                    func.min(reports.points).label("min_points"),
                    reports.reviewee).filter_by(tid=tids[i], is_final=False).filter(
                        reports.reviewee != reports.reviewer).group_by(reports.reviewee)
                # Query to get the students in the students table
                team_members = student.query.filter_by(tid=tids[i], session_id=session_id).distinct().all()
                if team_members is None:
                    team_members = []
            except exc.SQLAlchemyError:
                log_exception()
                return 'Error'

            temp = [team_names[i]]
            for team_member in team_members:
                # Checks whether the review is within the midterm dates
                if session.check_review_state(session_id, today) == "midterm":
                    for m in midterm_points:
                        if (team_member.id == m.reviewee):  # If the student's ID matches the review ID
                            params = {"name": team_member.name,
                                      "id": team_member.id,
                                      "active": "Midterm: ",
                                      "min_points": m.min_points,
                                      "max_points": m.max_points,
                                      "lead": int(team_member.is_lead)}
                            temp.append(params)
                            flag = 1
                # Checks whether the review is within the final dates
                elif session.check_review_state(session_id, today) == "final":
                    for f in final_points:
                        if (team_member.id == f.reviewee):  # If the student's ID matches the review ID
                            params = {"name": team_member.name,
                                      "id": team_member.id,
                                      "active": "Final: ",
                                      "min_points": f.min_points,
                                      "max_points": f.max_points,
                                      "lead": int(team_member.is_lead)}
                            temp.append(params)
                            flag = 1
                if flag == 0:
                    params = {"name": team_member.name,
                              "id": team_member.id,
                              "active": "",
                              "min_points": "",
                              "max_points": "",
                              "lead": int(team_member.is_lead)}
                    temp.append(params)
                flag = 0
            lists[i] = temp
        sessions = session.get_sessions()
        return lists, sessions

    def get_team_from_id(self, team_id):
        """
        Get the team object associated with the given id
        Input: team_id
        Output: a team object, if found. None otherwise
        """
        try:
            result = teams.query.filter(teams.id == team_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None
        return result

    # Return a tid.
    def get_tid_from_name(self, team_name, ses_id):
        """
        Get the team with the given name in the session identified by the given session id
        Input: self, team_name, session_id
        Output: the team, if we found it
        """
        try:
            result = teams.query.filter(teams.name == team_name,
                                        teams.session_id == ses_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None

        if result is not None:
            return result.id
        else:
            return None


class students(db.Model):
    __table__ = db.Model.metadata.tables['students']

    def check_dup_student(self, id, session_id):
        """
        Check if a student already exits in a session
        Input: id of the student and selected session id
        Output: return False if the student was already in
                return True otherwise
        """
        try:
            result = students.query.filter_by(id=id, session_id=session_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None
        if result is not None:
            return False
        return True

    def insert_student(self, name, email_address, id, session_id, t_name):
        """
        Add new student
        Input: student name, student email address, student id, team name and id of the selected session
        Output: return False if student id already exists in the current session
                add student to the database and return True otherwise
        """
        try:
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
        except exc.SQLAlchemyError:
            log_exception()
            return False

        return True

    def get_students(self, tid):
        """
        Get a list of the names of all students from a given team
        Input: team id, session id
        Output: list of student names, if everything succeeds. None otherwise
        """
        try:
            result = [r.name for r in students.query.filter_by(tid=tid)]
        except exc.SQLAlchemyError:
            log_exception()
            return None

        return result

    def get_team_members(self, tid):
        """
        Get all members of a team
        Input: team id as tid
        Output: A list of student objects representing the students on that team
        """
        try:
            mems = students.query.filter_by(tid=tid).distinct().all()
        except exc.SQLAlchemyError:
            log_exception()
            return None
        return mems

    def get_students_in_session(self, session_id):
        """
        Gets a list of students in the given session, ordered by team (in ascending order)
        Input: session_id
        Output: the list of students
        """
        # https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
        # https://docs.sqlalchemy.org/en/13/orm/query.html
        try:
            results = students.query.filter(
                          students.session_id == session_id).order_by(students.tid.asc()).all()
        except exc.SQLAlchemyError:
            log_exception()
            return None
        return results

    def get_user_sessions(self, student_id):
        """
        Returns all capstone sessions that a user belongs to
        Input: student_id: The database id of the student to retrieve capstone session ids for
        output: an array of objects representing the rows for each capstone the student belongs to
        """
        try:
            results = []  # to store objects

            # get all matching records
            student_records = students.query.filter_by(id=student_id).all()
            if student_records is not None:

                # for each record, add the capstone the id points to
                for rec in student_records:
                    cap = capstone_session().get_sess_by_id(rec.session_id)
                    if cap is not None:
                        results.append(cap)

            return results

        except exc.SQLAlchemyError:
            log_exception()
            return None

    def get_student_in_session(self, sid, session_id):
        """
        Get a student from the students table
        Input: student id, session id
        Output: the student that we found, or none if nothing was found
        """
        try:
            result = students.query.filter(students.id == sid, students.session_id == session_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None
        return result

    def remove_student(self, sts, t_name, session_id):
        """
        Remove a list of selected students
        Input: list of students, team name and session id
        Output: return False of the list of student is empty or if something went wrong
            otherwise, remove student from the team
        """
        try:
            if t_name is None or sts is None:
                return False
            removed_student = removed_students()
            team = teams.query.filter(teams.name == t_name,
                                      teams.session_id == session_id).first()
            for i in sts:
                student = students.query.filter(students.name == i,
                                                students.tid == team.id,
                                                students.session_id == session_id).first()
                removed_student.add_student(student)
                st = students.query.filter(students.id == student.id,
                                           students.session_id == session_id).first()
                db.session.delete(st)
                db.session.commit()
        except exc.SQLAlchemyError:
            log_exception()
            return False

        return True

    def validate(self, id):
        """
        validate cas username with student id in the database
        Input: student id
        Output: object of found student
        """
        try:
            result = students.query.filter_by(id=id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None

        if result is None:
            return False
        else:
            return result

    # Get the single student matching the id passed in
    # input: student id of the student to retrieve
    # output: the student's capstone session id value
    def get_student(self, s_id):
        try:
            return students.query.filter_by(id=s_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def update_team(self, name, s_id, t_id):
        try:
            students.query.filter_by(name=name,
                                     session_id=s_id).\
                                     update(dict(tid=t_id))
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            return False

    def check_team_lead(self, s_id, sess_id):
        """
        Check if the student passed in by id is the team lead
        Input: student id of the student to check
        Output: True if the student is a team lead, False otherwise
        """
        try:
            student = students.query.filter(students.id == s_id, students.session_id == sess_id).first()
            if student.is_lead == 1:
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            log_exception()
            return False

    def get_unassigned_students(self, s_id):
        """
        Get students from a session that do not have a team.
        Input: session id to grab students
        Output: Students who have no team.
        """
        try:
            empty_team = teams.query.filter_by(name="", session_id=s_id).first()
            if empty_team:
                return students.query.filter_by(session_id=s_id, tid=empty_team.id).all()
            else:
                return None
        # https://stackoverflow.com/questions/6470428/catch-multiple-exceptions-in-one-line-except-block
        except (exc.SQLAlchemyError, AttributeError):
            log_exception()
            return None

    def edit_student(self, id, new_name, new_email):
        """
        Allows students to edit their name and email address
        Input: student's new email and name and current user id
        Output: apply new name and email to students in student table
        """
        try:
            # Find the student
            student = students.query.filter(students.id == id).all()
            if student is None:
                return False

            # Change name and/or email, if either of them are non-blank
            for i in student:
                if new_name != '':
                    i.name = new_name
                if new_email != '':
                    i.email_address = new_email
                db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            return False

    def set_lead(self, session_id, team_name, lead):
        """
        Professor can set a lead for each team
        Input: self, chosen session id, team name and lead name
        Output: set 1 to team lead and 0 to the rest of students in the team
        """
        # Sanity check inputs
        if team_name is None or lead is None:
            return False

        # Set team lead status
        try:
            # Find the team
            team = teams.query.filter(teams.session_id == session_id, teams.name == team_name).first()
            if team is None:
                return False

            # Get list of students in the given team
            student = students.query.filter(students.tid == team.id).all()
            for i in student:
                if i.name == lead:
                    i.is_lead = 1
                else:
                    i.is_lead = 0
                db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            return False


class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']

    def get_max(self):
        """
        Calculate the next id for a newly added session
        if the table is empty, returns 1
        Otherwise, return the max id+1
        """
        try:
            max_id = db.session.query(func.max(capstone_session.id)).scalar()
        except exc.SQLAlchemyError:
            log_exception()
            max_id = None

        if max_id is None:
            return 1
        else:
            return max_id + 1

    def insert_session(self, term, year, professor_id):
        """
        Add a current session (only if it wasn't in the database)
        Input: starting term and year of the session
        Output: return id of the added session
        """
        term = term.strip().lower()
        year = year.strip().lower()
        e_term = None
        e_year = 0
        terms = ["fall", "winter", "spring", "summer"]
        for i in range(len(terms)):
            if terms[i] == term:
                e_term = terms[(i+1) % 4]
                e_term = e_term.capitalize()
        if term == 'fall':
            e_year = int(year)+1
        else:
            e_year = year
        id = self.get_max()
        term = term.capitalize()
        year = year.capitalize()
        prof_id = professor_id.lower()
        new_sess = capstone_session(id=id,
                                    start_term=term,
                                    start_year=year,
                                    end_term=e_term,
                                    end_year=e_year,
                                    professor_id=prof_id)
        db.session.add(new_sess)
        db.session.commit()
        return id

    def remove_session(self, session_id):
        """
        Removes an entire session with all the teams and students
        Input: session id
        """
        try:
            team = teams()
            session_teams = team.query.filter_by(session_id=session_id).all()
            del_session = capstone_session.query.filter(capstone_session.id == session_id).first()
            for t in session_teams:
                team_name = t.name
                team.remove_team_from_session(team_name, session_id)
            db.session.delete(del_session)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def get_sess_by_id(self, id):
        """
        Get the capstone session object associated with the given id
        inputs: id of capstone session to retrieve
        outputs: capstone session object if found, none otherwise
        """
        try:
            # query for session and return
            return capstone_session.query.filter_by(id=id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def check_term_name(self, s_term):
        """
        Checks if the name of the term is valid
        Input: start term of new session
        Output: return True if valid, False otherwise
        """
        s_term = s_term.strip().lower()
        terms = ["fall", "winter", "spring", "summer"]
        for i in range(len(terms)):
            if terms[i] == s_term:
                return True
        return False

    def check_term_year(self, s_year):
        """
        Checks if the year of the term is valid
        Input: start year of new session
        Output: return False if invalid, True otherwise
        """
        check_year = s_year.isdigit()
        if not check_year:
            return False
        return True

    def check_session_id_valid(self, v_id):
        """
        Checks if the returned session ID is greater than
        or equal to 0
        """
        check_id = v_id.isdigit()
        if check_id < 0:
            return False
        return True

    def check_dup_session(self, s_term, s_year, p_id):
        """
        Check if the new session name already exists in the database
        Input: start term & year of the new session
        Output: return False if the team already exists, True otherwise
        """
        try:
            s_term = s_term.strip().lower().capitalize()
            s_year = s_year.strip().lower().capitalize()
            p_id = p_id.strip().lower()
            result = capstone_session().query.filter_by(
                start_term=s_term, start_year=s_year, professor_id=p_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            result = None

        if result is not None:
            return False
        return True

    def get_session_id(self, term, year, prof):
        """
        Get id of a selected session
        Input: term and year
        Output: if the term and year are not found, add them to the database and
             return added session id. Otherwise, return the id of the session
        """
        prof_id = professors().prof_id(prof)
        try:
            id = capstone_session.query.filter(capstone_session.start_term == term,
                                               capstone_session.start_year == year,
                                               capstone_session.professor_id == prof_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            id = None

        if id is None:
            prof_id = professors().prof_id(prof)
            return self.insert_session(term, str(year), prof_id)
        else:
            return id.id

    def get_sessions(self):
        """
        Get a list of session to display on the drop downs
        Input: only self
        Output: list of sessions (includes start term, year and professor name)
        """
        caps = capstone_session.query.all()
        lists = []
        for i in caps:
            prof = professors.query.filter(professors.id == i.professor_id).first()
            temp = str(i.start_term) + " - " + str(i.start_year) + " (" + str(prof.name) + ")"
            lists.append(temp)
        return lists

    def get_active_sessions(self):
        """
        Get a list of active capstone sessions
        Input: self
        Output: the list of currently active capstone sessions
        """
        # Calculate the start term and year of the sessions we expect to be active
        currentDate = datetime.datetime.now()
        month = int(currentDate.month)
        if month in range(1, 3):
            # Fall term of last year
            start_term_1 = "Fall"
            start_year_1 = currentDate.year - 1

            # Winter term of current year
            start_term_2 = "Winter"
            start_year_2 = currentDate.year
        else:
            # Both terms will start in the same year
            start_year_1 = currentDate.year
            start_year_2 = currentDate.year

            # Winter and Spring terms
            if month in range(3, 6):
                start_term_1 = "Winter"
                start_term_2 = "Spring"
            # Spring and Summer terms
            elif month in range(6, 9):
                start_term_1 = "Spring"
                start_term_2 = "Summer"
            # Summer and Fall terms
            else:
                start_term_1 = "Summer"
                start_term_2 = "Fall"

        # Query the db for active sessions using the start term and year information we calculated above
        try:
            # https://stackoverflow.com/questions/7942547/using-or-in-sqlalchemy
            # Algorithm: SELECT * FROM CAPSTONE_SESSION WHERE
            #               (start_term = start_term_1 AND start_year = start_year_1)
            #                 OR
            #               (start_term = start_term_2 AND start_year = start_year_2)
            return capstone_session.query.filter(((capstone_session.start_year == start_year_1) &
                                                  (capstone_session.start_term == start_term_1)) |
                                                 ((capstone_session.start_year == start_year_2) &
                                                  (capstone_session.start_term == start_term_2))).all()
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def check_dates(self, start, end):
        """
        Check if start and end dates are valid
        Input: start and end dates
        Output: Return 0 if valid, return 1 if start date is after the end date
                Return 1 if either start or end date is empty
        """
        params = {'start': start, 'end': end}
        if params['start'] and params['end']:
            if int(params['start']) > int(params['end']):
                return 1
            else:
                return 0
        elif params['start'] is None and params['end'] is None:
            return 0
        return 2

    def date_error(self, params):
        """
        This method handles error message for inserting dates
        Input: parameter of dates (start/end dates for midterm/final)
        Output: error message
        """
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

    def split_dates(self, params):
        """
        Split dates into integer year, month and day
        to convert the string to datetime object
        Input: parameter of dates
        Outout: parameter of datetime objects
        """
        for i in params:
            if params[i]:
                params[i] = params[i].split('-')
                params[i] = datetime.datetime(int(params[i][0]), int(params[i][1]), int(params[i][2]))
            else:
                params[i] = None
        return params

    def insert_dates(self, midterm_start, midterm_end, final_start, final_end, session_id):
        """
        Insert a start and end date for midterm and final review
        Input: start and end date for midterm review and final reviews
        Output: update the dates in the database
        """
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

    def check_review_state(self, session_id, date):
        """
        Given a capstone session id to check and a date,
        this method determines the currently available review if any
        Inputs: a capstone session id and a date which should be a python date time object
        Outputs: 'final' if date is after the final start date for the session
        'midterm' if the date is between the midterm and final start dates.
        'error' otherwise
        """
        try:
            # get the session
            session = capstone_session.query.filter(capstone_session.id == session_id).first()
            # check if final exists:
            if session.final_start is not None:
                # if after final period, return final
                if date >= session.final_start:
                    return 'final'
                elif session.midterm_start is not None:
                    # otherwise if midterm exists, check if after midterm and return if so
                    if date >= session.midterm_start:
                        return 'midterm'
                else:
                    return 'Error'

            elif session.midterm_start is not None:
                # if only midterm exists, check midterm
                if date >= session.midterm_start:
                    return 'midterm'

            else:
                # no dates set, so error
                return 'Error'
        except exc.SQLAlchemyError:
            log_exception()
            return 'Error'

    def check_not_late(Self, session_id, date, type):
        """
        This method is for determining is a review is late. It receives the type of review to check
        and compares the date sent into the method with the review's end period
        Inputs: session_id -- the value of the id for the capstone session to check
        date: the date that the review is submitted, type: "midterm" or "final" should be received
        Outputs: True -- the review is within the open period (the review is NOT late)
        or False -- the review IS late or an error was experienced
        """
        try:
            # get the session
            session = capstone_session.query.filter(capstone_session.id == session_id).first()

            # check the type:

            if type == 'midterm':
                # check if midterm date exists
                if session.midterm_end is not None:
                    # check date to see if its currently or before the midterm start state
                    if date <= session.midterm_end:
                        # on time
                        return True
                    else:
                        # late
                        return False
                else:
                    # error
                    return False
            elif type == 'final':
                # check if final date exists
                if session.final_end is not None:
                    # check date
                    if date <= session.final_end:
                        # on time
                        return True
                    else:
                        # late
                        return False
                else:
                    # error
                    return False
            else:
                # error
                return False
        except exc.SQLAlchemyError:
            log_exception()
            return False


class reports(db.Model):
    __table__ = db.Model.metadata.tables['reports']

    def get_reports_for_student(self, student_id, session_id, is_final=None):
        """
        Gets all available reports for a student, optionally filtering to only midterms or finals
        Input: student id, session_id and is_final (is_final indicates if we are filtering for final reviews
               or not. is_final = true indicates we are looking for final reviews. is_final = false indicates
               we are looking for midterm reviews. is_final = None indicates we want both.
        Output: the available reports for the student
        """
        try:
            reviews = {}
            if is_final is not None:
                reviews = reports.query.filter(reports.reviewee == student_id,
                                               reports.session_id == session_id,
                                               reports.is_final == is_final).all()
            else:
                reviews = reports.query.filter(reports.reviewee == student_id,
                                               reports.session_id == session_id).all()
            return reviews
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def get_report(self, reviewer_id, reviewee_id, team_id, is_final):
        """
        Get a review from the database using the given information
        Input: reviewer_id (a student id), reviewee_id (a student id), team_id, is_final (indicates if the
               review is a final review or not)
        Output: the review, if it was found, or None if it wasn't or if there was a problem
        """
        try:
            return reports.query.filter(reports.reviewer == reviewer_id,
                                        reports.tid == team_id,
                                        reports.is_final == is_final,
                                        reports.reviewee == reviewee_id).first()
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def get_team_reports(self, tid, is_final):
        """
        This method is for getting the reports of an entire team
        Inputs: tid -- team id of reports to retrieve, is_final - if it's the second term
        Outputs: result - all report objects for the team
        """
        try:
            result = reports.query.filter(reports.tid == tid,
                                          reports.is_final == is_final).distinct().all()
            return result
        except exc.SQLAlchemyError:
            log_exception()
            return None

    def insert_report(self, sess_id, time, reviewer, tid, reviewee, tech,
                      ethic, com, coop, init, focus, cont, lead, org, dlg,
                      points, strn, wkn, traits, learned, proud, is_final, late):
        """
        Stages a report to be inserted into the database -- This does NOT commit the add!
        Inputs: Arguments for each individual field of the report
        Outputs: true if adding was successful, false if not
        """
        try:
            # Build Report object from method input
            new_report = reports(session_id=sess_id,
                                 time=time,
                                 reviewer=reviewer,
                                 tid=tid,
                                 reviewee=reviewee,
                                 tech_mastery=tech,
                                 work_ethic=ethic,
                                 communication=com,
                                 cooperation=coop,
                                 initiative=init,
                                 team_focus=focus,
                                 contribution=cont,
                                 leadership=lead,
                                 organization=org,
                                 delegation=dlg,
                                 points=points,
                                 strengths=strn,
                                 weaknesses=wkn,
                                 traits_to_work_on=traits,
                                 what_you_learned=learned,
                                 proud_of_accomplishment=proud,
                                 is_final=is_final,
                                 is_late=late)
            # add the report and return true for success
            db.session.add(new_report)
            print('Adding Report to Session')
            return True
        except exc.SQLAlchemyError:
            # if error, return false
            log_exception()
            return False

    def commit_reports(self, id, state, sess_id, success):
        """
        Method to commit changes to the DB through the model while updating the user's state
        input: None
        output: True if successful, false otherwise
        """
        # if adding reports was not successful, rollback changes to session
        try:
            if success is False:
                try:
                    print('Rolling Back Reports')
                    db.session.rollback()
                except exc.SQLAlchemyError:
                    return False
                return False

            # update appropriate student 'done' attribute
            print('Finding Student')
            student = students.query.filter_by(id=id, session_id=sess_id).first()
            if state == 'midterm':
                student.midterm_done = 1
            elif state == 'final':
                student.final_done = 1
            else:
                return False

            print('Committing Reports')

            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            log_exception()
            print('Rolling Back Reports')
            db.session.rollback()
            return False

    def commit_updates(self, success):
        """
        This method is for committing review updates
        input: success -- a boolean object indicating whether to proceed
        with committing (true) or to roll back (false)
        output: False -- commit was not made, True - commit was made successfully
        """
        try:
            if success is False:
                print('Rolling Back Edits')
                db.session.rollback()
                return False
            else:
                print('Committing Edits')
                db.session.commit()
                return True
        except exc.SQLAlchemyError:
            log_exception()
            print('Rolling Back Edits')
            db.session.rollback()
            return False


class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    def add_student(self, s):
        """
        Insert removed students into remocved_students table
        Input: student info
        Output: return False if the info is empty
                Otherwise, add student to the list and return True
        """
        if s is None:
            return False
        current_date = datetime.datetime.now()
        removed_student = removed_students(id=s.id,
                                           tid=s.tid,
                                           session_id=s.session_id,
                                           name=s.name,
                                           is_lead=s.is_lead,
                                           midterm_done=s.midterm_done,
                                           final_done=s.final_done,
                                           removed_date=current_date)
        db.session.add(removed_student)
        db.session.commit()
        return True
