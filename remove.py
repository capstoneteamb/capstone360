from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import removeDashboard
import gbmodel
import datetime

class RemoveStudent(MethodView):
    def get(self):
        return render_template('removeStudent.html')

    def post(self):
   
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

        students = request.form.getlist('removedStudent')
        #TODO: assume the student name is unique //
        student.removeStudent(students, sessionID)
        lists = removeDashboard.get_rm()
        # print(lists)
        return render_template('removeDashboard.html', lists = lists) 


class RemoveTeam(MethodView):
    def get(self):
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        return render_template('removeTeam.html', tName = tName)

    def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """

        session = gbmodel.capstone_session()
        team = gbmodel.teams()

        currentDate = datetime.datetime.now()
        month = int(currentDate.month) 
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"

        sessionID = session.getSessionID(term, year)

        tName = request.form.get('teamName')
        tName = tName.replace("_", " ")
        team.removeTeam(tName, sessionID)
        lists = removeDashboard.get_rm()
        return render_template('removeDashboard.html', lists = lists) 

