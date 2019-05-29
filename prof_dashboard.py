"""
This file includes the professor dashboard and
handles get post request for proDashboard.html
"""
from flask import request, render_template
from flask.views import MethodView
import gbmodel
import datetime
from catCas import validate_professor
from flask_cas import login_required
import logging
from sqlalchemy.exc import SQLAlchemyError
import csv
import io
import re


class ProfDashboard(MethodView):
    """
    ProfDashboard class handles get and post requests for profDashboard.html
    """
    def valid_email(self, email):
        """
        Verify if the email is in a correct syntax by checking if it has '@' & '.'
        Input: self and new email
        Output: return True if it matches the format, False otherwise
        """
        if len(email) > 7:
            if re.match('^[_a-z0-9-]+(|.[_a-z0-9-]+)*@[a-z0-9-]+'
                        '(|.[a-z0-9-]+)*(|.[a-z]{2,4})$', email) is not None:
                return True
        return False

    @login_required
    def get(self):
        """
        Get session_id from the prefvious selected session
        If None returned then request for a selection.
        Otherwise, display the current session_id
        """
        if validate_professor() is False:
            msg = "Professor not found"
            return render_template('errorMsg.html', msg=msg)
        session = gbmodel.capstone_session()
        team = gbmodel.teams()
        session_id = request.args.get('session_id')
        if session_id is None:
            user_session = request.args.get('selected_session')
            if user_session is not None:
                user_session = user_session.split('-')
                term = str(user_session[0].strip())
                year = int(user_session[1][:5].strip())
                prof = str(user_session[1][7:-1])
            else:
                current_date = datetime.datetime.now()
                month = int(current_date.month)
                year = current_date.year
                if month in range(9, 11):
                    term = "Fall"
                elif month in range(3, 6):
                    term = "Spring"
                elif month in range(6, 9):
                    term = "Summer"
                else:
                    term = "Winter"
                prof = validate_professor().name
            session_id = session.get_session_id(term, year, prof)
        # Lists - a list of teams and students of a selected session to display on the dashboard
        # Sessions - a list of sessions to display in drop downs
        lists, sessions = team.dashboard(session_id)
        return render_template('profDashboard.html', lists=lists, sessions=sessions, session_id=session_id)

    def post(self):
        """
        This method handles all the functionalities from proDashboard
        includes add/remove students/teams, add new session, set review
        midterm/final start/end dates and set team lead
        """
        session = gbmodel.capstone_session()
        student = gbmodel.students()
        team = gbmodel.teams()
        professor = gbmodel.professors()
        # Get current session id from dropdowns in profDashboard.html
        session_id = request.form['session_id']
        session_id = int(session_id)
        if 'student_name' in request.form:
            # Add New Student (student name, student id and student email)
            # Get team name and session id from profDashboard.html,
            # new student id, name, email from addStudent.html
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            if not student.check_dup_student(request.form['student_id'], session_id):
                # If student id in a current session already exists
                # Return to addStudent.html with error msg and request a new form
                error = "Student id " + str(request.form['student_id']) + " already exists"
                team_name = team_name.replace(" ", "_")
                return render_template('addStudent.html',
                                       team_name=team_name,
                                       session_id=session_id,
                                       error=error)
            if request.form['student_email'] != '':
                # If new email is invalid, return to addStudent.html
                # with error msg and request a new form
                if self.valid_email(str(request.form['student_email'])) is False:
                    error = "Invalid Email Address"
                    team_name = team_name.replace(" ", "_")
                    return render_template('addStudent.html',
                                           team_name=team_name,
                                           session_id=session_id,
                                           error=error)
            # Insert new student information into the database
            student.insert_student(request.form['student_name'],
                                   request.form['student_email'],
                                   request.form['student_id'],
                                   session_id,
                                   team_name)
            # Update new list of students to reflect on profDashboard.html
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        elif 'team' in request.form:
            # Remove a student/students from a team
            # get list of students and team name from profDashboard.html
            students = request.form.getlist('removed_student')
            team_name = request.form.get('team')
            team_name = team_name.replace("_", " ")
            # Remove student/students from database
            student.remove_student(students, team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        elif 'removed_team' in request.form:
            # Remove a team in a session
            # Get team name in current session from profDashboard.html
            team_name = request.form.get('removed_team')
            # There was a problem removing teams with blank names, so (in remove team requests) a '_'
            # character was added to the beginning of the name. We will want to remove it before we continue
            # https://stackoverflow.com/questions/4945548/remove-the-first-character-of-a-string
            team_name = team_name[1:]
            team_name = team_name.replace("_", " ")
            # Remove team and students in the team from database
            team.remove_team(team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        elif 'start_term' in request.form:
            # Add a new session to the profDashboard
            while not session.check_term_name(request.form['start_term']):
                error = "Enter a valid term (Example: Summer)"
                return render_template('addSession.html', error=error, session_id=session_id)
            while not session.check_term_year(request.form['start_year']):
                error = "Enter a valid year (Example: 2019)"
                return render_template('addSession.html', error=error, session_id=session_id)
            while not professor.check_professor(request.form['professor_id']):
                error = "Enter a valid professor ID"
                return render_template('addSession.html', error=error, session_id=session_id)
            while not session.check_dup_session(request.form['start_term'], request.form['start_year'],
                                                request.form['professor_id']):
                error = "Session already exists"
                return render_template('addSession.html', error=error, session_id=session_id)
            start_term = request.form.get('start_term')
            start_year = request.form.get('start_year')
            start_term = start_term.replace("_", " ")
            start_year = start_year.replace("_", " ")
            professor_id = request.form.get('professor_id')
            professor_id = professor_id.replace("_", " ")
            session_id = session.insert_session(start_term, start_year, professor_id)
            lists, sessions = team.dashboard(session_id)
            return render_template(
                'profDashboard.html', lists=lists, sessions=sessions, session_id=session_id)
        # If REMOVE SESSION was submitted (removed_session)
        elif 'removed_session' in request.form:
            while not session.check_session_id_valid(request.form['removed_session']):
                error = "Invalid session ID"
                return render_template('profDashboard.html',
                                       lists=lists, sessions=sessions, session_id=session_id)
            remove_session = request.form.get('removed_session')
            remove_session = remove_session.replace("_", " ")
            session.remove_session(session_id)
            session_id = session.get_max() - 1
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # If ADD TEAM was submitted (addTeam)
        elif 'team_name' in request.form:
            # Add a new team to a current session
            # Request new team name from addTeam.html
            if not team.check_dup_team(request.form['team_name'], session_id):
                # If new name already exists in current session
                # Rentering the addTeam.html with given error message
                error = "Team name already exists"
                return render_template('addTeam.html', error=error, session_id=session_id)
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            # Add new team to the given session from profDashboard.html
            team.insert_team(session_id, team_name)
            # Update new list of sessions, teams, students to reflect on profDashboard.html
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # if ASSIGNED TEAMS for to place new students on teams was submitted
        elif 'assigned_teams' in request.form:
            size = request.form.get('size')
            size = int(size)
            unassigned_students = student.get_unassigned_students(session_id)
            team_names = []
            i = 1
            while i <= size:
                team_name = (request.form.get('assigned_team'+str(i)))
                if team.check_dup_team(team_name, session_id) is False:
                    t_id = team.get_tid_from_name(team_name, session_id)
                    student.update_team(unassigned_students[i-1].name,
                                        session_id, t_id)
                else:
                    team.insert_team(session_id, team_name)
                    t_id = team.get_tid_from_name(team_name, session_id)
                    student.update_team(unassigned_students[i-1].name,
                                        session_id, t_id)
                team_names.append(team_name)
                i += 1
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # If IMPORT STUDENTS was submitted (addTeamCSV)
        elif 'student_data_csv' in request.files:
            session_id = int(request.form['session_id'])
            teams_table = gbmodel.teams()  # Accessor to the teams table
            students_table = gbmodel.students()  # Accessor to the students table
            file = request.files['student_data_csv']
            # If 'Create from File' was selected with no file
            # return back to import student page.
            if(file.filename == ''):
                return render_template('csvAddTeam.html',
                                       session_id=session_id,
                                       error="Please select a file to upload")
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(stream, delimiter=',')
            uninserted_students = []
            for row in csv_reader:
                student_name = row[0]
                student_id = row[1]
                team_name = row[2]

                # Create team if it doesn't exist, then create the student.
                try:
                    if teams_table.check_dup_team(team_name, session_id) is True:
                        teams_table.insert_team(session_id, team_name)
                except SQLAlchemyError:
                    logging.error(('CSV Add Students/Team - Error checking for existing team and/or'
                                   ' inserting a new one'))
                    return render_template('csvAddTeam.html',
                                           session_id=session_id,
                                           error="Something went wrong")
                try:
                    if students_table.get_student_in_session(student_id, session_id) is None:
                        students_table.insert_student(student_name, "", student_id, session_id, team_name)
                    else:
                        # Keep track of what students weren't added to the database (and make a note it)
                        logging.warning("CSV Add Students/Team - Error inserting student into the database")
                        uninserted_students.append(student_name)
                except SQLAlchemyError:
                    logging.error(('CSV Add Students/Team -'
                                   ' Error inserting students or checking if they exist in the database'))
                    return render_template('csvAddTeam.html',
                                           session_id=session_id,
                                           error="Something went wrong")

            # If everything went well, reload the professor dashboard
            if uninserted_students is None:
                logging.info("CSV Add Students/Team - added student data from uploaded csv file")
                lists, sessions = team.dashboard(session_id)
                return render_template('profDashboard.html',
                                       lists=lists,
                                       sessions=sessions,
                                       session_id=session_id)
            # If there were some problems, let the user know
            else:
                error_str = "There was a problem inserting the following students into the database: "
                error_str = error_str + ", ".join(uninserted_students)
                error_str = error_str + ". They are already in this session."
                return render_template('csvAddTeam.html',
                                       session_id=session_id,
                                       error=error_str)

        # If SET DATE for reviews was submitted (setDate)
        elif 'midterm_start' in request.form:
            # Add midterm/final start/end dates for review form
            # Request start and end dates for midterm and final from setDate.html
            midterm_start = request.form.get('midterm_start')
            midterm_end = request.form.get('midterm_end')
            final_start = request.form.get('final_start')
            final_end = request.form.get('final_end')
            params = {'midterm_start': midterm_start,
                      'midterm_end': midterm_end,
                      'final_start': final_start,
                      'final_end': final_end}
            if session.date_error(params) is not None:
                # Check if the dates are valid, rendering to setDate.html
                # with a error message
                error_msg = session.date_error(params)
                return render_template('setDate.html', error=error_msg, session_id=session_id)
            # Insert dates into database
            session.insert_dates(midterm_start, midterm_end, final_start, final_end, session_id)
            # Update new list of sessions, teams, students to reflect on profDashboard.html
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        elif 'team_lead' in request.form:
            # Set team lead for a team in current session
            # Get team name and lead from checkboxes in profDashboard.html
            team_name = request.form.get('team_lead')
            student_name = request.form.get('is_lead')
            team_name = team_name.replace("_", " ")
            # Set lead for chosen team in current sesison
            student.set_lead(session_id, team_name, student_name)
            # Update new list of sessions, teams, students to reflect on profDashboard.html
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)


class AddStudent(MethodView):
    """
    This class handles get requests for addStudent.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go addStudent.html
        Input: only self
        Output: rendering the addSession.html template with session id
                name of the team from profDashboard.html
        """
        team_name = request.args.get('data')
        team_name = team_name.replace(" ", "_")
        session_id = request.args.get('session_id')
        return render_template('addStudent.html', team_name=str(team_name), session_id=session_id, error=None)


class AddSession(MethodView):
    """
    This class handles get requests for addStudent.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go addSession.html
        Input: only self
        Output: rendering the addSession.html template with session id
                from profDashboard.html
        """
        session_id = request.args.get('session_id')
        return render_template('addSession.html', error=None, session_id=session_id)


class RemoveSession(MethodView):
    """
    This class handles get requests for removeSession.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go removeSession.html
        Input: only self
        Output: rendering the removeSession.html template with session id
                from profDasboard.html
        """
        session_id = request.args.get('session_id')
        return render_template('removeSession.html', error=None, session_id=session_id)


class AddTeam(MethodView):
    """
    This class handles get requests for addTeam.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go addTeam.html
        Input: only self
        Output: rendering the addSession.html template with session id
                from profDashboard.html
        """
        session_id = request.args.get('session_id')
        return render_template('addTeam.html', error=None, session_id=session_id)


# Create a webpage for professors to import students
# via csv file.
class AddTeamCSV(MethodView):
    @login_required
    # Display webpage
    def get(self):
        session_id = request.args.get('session_id')
        return render_template('csvAddTeam.html', session_id=session_id)


class RemoveTeam(MethodView):
    """
    This class handles get requests for removeTeam.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go removeTeam.html
        Input: only self
        Output: rendering the addSession.html template with session id
                and team name from profDashboard.html
        """
        team_name = request.args.get('data')
        team_name = team_name.replace(" ", "_")
        session_id = request.args.get('session_id')
        return render_template('removeTeam.html', team_name=team_name, session_id=session_id)


class SetDate(MethodView):
    """
    This class handles get requests for setDate.html
    """
    @login_required
    def get(self):
        """
        This method handles get requests go setDate.html
        Input: only self
        Output: rendering the addSession.html template with session id
                from profDashboard.html
        """
        session_id = request.args.get('session_id')
        return render_template('setDate.html', error=None, session_id=session_id)


class AssignTeam(MethodView):
    @login_required
    def get(self):
        s_id = request.args.get('session_id')
        if validate_professor is False:
            msg = "Professor not found"
            return render_template('errorMsg.html', msg=msg)
        students_table = gbmodel.students()
        team_table = gbmodel.teams()
        unassigned_students = students_table.get_unassigned_students(s_id)
        if unassigned_students is None:
            error = "No students unassigned to a team."
            return render_template('errorPage.html', msg=error)
        sessions = team_table.dashboard(s_id)
        return render_template('assignTeam.html',
                               lists=unassigned_students,
                               sessions=sessions,
                               session_id=s_id,
                               error=None)
