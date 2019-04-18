from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
import dashboard

class AddStudent(MethodView):
    def get(self):
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        return render_template('addStudent.html', tName = str(tName), error=None)

    def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """
        session = gbmodel.capstone_session()
        student = gbmodel.students()

        currentDate = datetime.datetime.now()
        month = int(currentDate.month) 
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"

        sessionID = session.getSessionID(term, year)
        teamName = request.form.get('teamName')
        tName = teamName.replace("_", " ")
        while student.checkDupStudent(request.form['studentID'], sessionID):
            student.insertStudent(request.form['studentName'], request.form['studentID'], sessionID, tName)
            lists = dashboard.get()
            return render_template('dashboard.html', lists = lists)
        error = "Student id "+ str(request.form['studentID']) + " already exists"
        return render_template('addStudent.html', tName = teamName, error=error)


class AddTeam(MethodView):
    def get(self):
        error = None
        return render_template('addTeam.html', error=error)

    def post(self):
        session = gbmodel.capstone_session()
        team = gbmodel.teams()
        error = None
        currentDate = datetime.datetime.now()
        month = int(currentDate.month) 
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"

        sessionID = session.getSessionID(term, year)
        while team.checkDupTeam(request.form['teamName'], sessionID):
            team.insertTeam(sessionID,request.form['teamName']) 
            lists = dashboard.get()
            return render_template('dashboard.html', lists = lists) 
        error = "Team name already exists"
        return render_template('addTeam.html', error=error)
