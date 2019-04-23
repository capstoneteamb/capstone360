from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
import dashboard

class AddStudent(MethodView):
    def get(self):
        t_name = request.args.get('data')
        t_name = t_name.replace(" ", "_")
        return render_template('addStudent.html', t_name = str(t_name), error=None)

    def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """
        session = gbmodel.capstone_session()
        student = gbmodel.students()

        current_date = datetime.datetime.now()
        month = int(current_date.month) 
        year = current_date.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"

        session_id = session.get_session_id(term, year)
        teamName = request.form.get('teamName')
        t_name = teamName.replace("_", " ")
        while student.check_dup_student(request.form['studentID'], session_id):
            student.insert_student(request.form['student_name'], request.form['studentID'], session_id, t_name)
            lists = dashboard.get()
            return render_template('dashboard.html', lists = lists)
        error = "Student id "+ str(request.form['studentID']) + " already exists"
        return render_template('addStudent.html', t_name = teamName, error=error)


class AddTeam(MethodView):
    def get(self):
        error = None
        return render_template('addTeam.html', error=error)

    def post(self):
        session = gbmodel.capstone_session()
        team = gbmodel.teams()
        error = None
        current_date = datetime.datetime.now()
        month = int(current_date.month) 
        year = current_date.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"

        session_id = session.get_session_id(term, year)
        while team.check_dup_team(request.form['teamName'], session_id):
            team.insert_team(session_id,request.form['teamName']) 
            lists = dashboard.get()
            return render_template('dashboard.html', lists = lists) 
        error = "Team name already exists"
        return render_template('addTeam.html', error=error)
