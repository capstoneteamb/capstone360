from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime

class RemoveStudent(MethodView):
    def get(self):
        return render_template('removeStudent.html')

    def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        currentDate = datetime.datetime.now()
        month = int(currentDate.month)      
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"
        sessionID = model.getSessionID(term, year)
        students = request.form.getlist('removedStudent')
        #TODO: assume the student name is unique //
        model.removeStudent(students, sessionID[0])
        return redirect(url_for('removeDashboard' ))


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

        model = gbmodel.get_model()
        currentDate = datetime.datetime.now()
        month = int(currentDate.month)      
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"
        sessionID = model.getSessionID(term, year)
        tName = request.form.get('teamName')
        tName = tName.replace("_", " ")
        model.removeTeam(tName, sessionID[0])
        return redirect(url_for('removeDashboard'))

