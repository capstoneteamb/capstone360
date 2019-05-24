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


class ProfDashboard(MethodView):
    @login_required
    def get(self):
        if validate_professor() is False:
            msg = "Professor not found"
            return render_template('errorMsg.html', msg=msg)
        session = gbmodel.capstone_session()
        team = gbmodel.teams()
        # Get session_id from the prefvious selected session
        # If None returned then request for a selection.
        # Otherwise, display the current session_id
        session_id = request.args.get('session_id')
        if session_id is None:
            user_session = request.args.get('selected_session')
            if user_session is not None:
                user_session = user_session.split('-')
                term = str(user_session[0].strip())
                year = int(user_session[1].strip())
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
            session_id = session.get_session_id(term, year)
        # Lists - a list of teams and students of a selected session to display on the dashboard
        # Sessions - a list of sessions to display in drop downs
        lists, sessions = team.dashboard(session_id)
        return render_template('profDashboard.html', lists=lists, sessions=sessions, session_id=session_id)

    def post(self):
        session = gbmodel.capstone_session()
        student = gbmodel.students()
        team = gbmodel.teams()
        session_id = request.form['session_id']
        session_id = int(session_id)
        # If ADD STUDENT form was submitted (addStudent)
        if 'student_name' in request.form:
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            if not student.check_dup_student(request.form['student_id'], session_id):
                error = "Student id " + str(request.form['student_id']) + " already exists"
                team_name = team_name.replace(" ", "_")
                return render_template('addStudent.html',
                                       team_name=team_name,
                                       session_id=session_id,
                                       error=error)
            student.insert_student(request.form['student_name'],
                                   request.form['student_email'],
                                   request.form['student_id'],
                                   session_id,
                                   team_name)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # If REMOVE STUDENT was submitted (in dashboard)
        elif 'team' in request.form:
            students = request.form.getlist('removed_student')
            team_name = request.form.get('team')
            team_name = team_name.replace("_", " ")
            student.remove_student(students, team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # If REMOVE TEAM was submitted (removed_team)
        elif 'removed_team' in request.form:
            team_name = request.form.get('removed_team')
            team_name = team_name.replace("_", " ")
            team.remove_team(team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)
        # If ADD TEAM was submitted (addTeam)
        elif 'team_name' in request.form:
            if not team.check_dup_team(request.form['team_name'], session_id):
                error = "Team name already exists"
                return render_template('addTeam.html', error=error, session_id=session_id)
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            team.insert_team(session_id, team_name)
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
            midterm_start = request.form.get('midterm_start')
            midterm_end = request.form.get('midterm_end')
            final_start = request.form.get('final_start')
            final_end = request.form.get('final_end')
            params = {'midterm_start': midterm_start,
                      'midterm_end': midterm_end,
                      'final_start': final_start,
                      'final_end': final_end}
            if session.date_error(params) is not None:
                error_msg = session.date_error(params)
                return render_template('setDate.html', error=error_msg, session_id=session_id)
            session.insert_dates(midterm_start, midterm_end, final_start, final_end, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('profDashboard.html',
                                   lists=lists,
                                   sessions=sessions,
                                   session_id=session_id)


class AddStudent(MethodView):
    @login_required
    def get(self):
        # Get team_id, team name and session id from dashboard
        team_name = request.args.get('data')
        team_name = team_name.replace(" ", "_")
        session_id = request.args.get('session_id')
        return render_template('addStudent.html', team_name=str(team_name), session_id=session_id, error=None)


class AddTeam(MethodView):
    @login_required
    def get(self):
        # Get seesion id from dashboard
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
    @login_required
    def get(self):
        # Get team name, the spaces were replaced with '_' in order to keep the entire name.
        # Otherwise the part after spaces would be cut (for some reason)
        # Also, Get session id from dashboard
        team_name = request.args.get('data')
        team_name = team_name.replace(" ", "_")
        session_id = request.args.get('session_id')
        return render_template('removeTeam.html', team_name=team_name, session_id=session_id)


class SetDate(MethodView):
    @login_required
    def get(self):
        session_id = request.args.get('session_id')
        return render_template('setDate.html', error=None, session_id=session_id)
