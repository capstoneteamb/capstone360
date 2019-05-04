from flask import request, render_template
from flask.views import MethodView
import gbmodel
import datetime
from catCas import validate
from flask_cas import login_required


class Dashboard(MethodView):
    @login_required
    def get(self):
        if validate() is False:
            return render_template('index.html')
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
        return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)

    def post(self):
        session = gbmodel.capstone_session()
        student = gbmodel.students()
        team = gbmodel.teams()
        session_id = request.form['session_id']
        session_id = int(session_id[0])
        # If ADD STUDENT form was submitted (addStudent)
        if 'student_name' in request.form:
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            while not student.check_dup_student(request.form['student_id'], session_id):
                error = "Student id " + str(request.form['student_id']) + " already exists"
                team_name = team_name.replace(" ", "_")
                return render_template('addStudent.html', team_name=team_name, session_id=session_id, error=error)
            student.insert_student(request.form['student_name'], request.form['student_id'], session_id, team_name)
            lists, sessions = team.dashboard(session_id)
            return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)
        # If REMOVE STUDENT was submitted (in dashboard)
        elif 'team' in request.form:
            students = request.form.getlist('removed_student')
            team_name = request.form.get('team')
            team_name = team_name.replace("_", " ")
            student.remove_student(students, team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)
        # If REMOVE TEAM was submitted (removed_team)
        elif 'removed_team' in request.form:
            team_name = request.form.get('removed_team')
            team_name = team_name.replace("_", " ")
            team.remove_team(team_name, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)
        # If ADD TEAM was submitted (addTeam)
        elif 'team_name' in request.form:
            while not team.check_dup_team(request.form['team_name'], session_id):
                error = "Team name already exists"
                return render_template('addTeam.html', error=error, session_id=session_id)
            team_name = request.form.get('team_name')
            team_name = team_name.replace("_", " ")
            team.insert_team(session_id, team_name)
            lists, sessions = team.dashboard(session_id)
            return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)
        # If SET DATE for reviews was submitted (setDate)
        elif 'midterm_start' in request.form:
            midterm_start = request.form.get('midterm_start')
            midterm_end = request.form.get('midterm_end')
            final_start = request.form.get('final_start')
            final_end = request.form.get('final_end')
            params = {'midterm_start': midterm_start, 'midterm_end': midterm_end, 'final_start': final_start, 'final_end': final_end}
            while session.date_error(params) is not None:
                error_msg = session.date_error(params)
                return render_template('setDate.html', error=error_msg, session_id=session_id)
            session.insert_dates(midterm_start, midterm_end, final_start, final_end, session_id)
            lists, sessions = team.dashboard(session_id)
            return render_template('dashboard.html', lists=lists, sessions=sessions, session_id=session_id)


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
