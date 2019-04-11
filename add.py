from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
#test

class AddStudent(MethodView):
    def get(self):
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        return render_template('addStudent.html', tName = str(tName))

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
        model.insertStudent(request.form['studentName'], request.form['studentID'], sessionID[0], tName)
        return redirect(url_for('dashboard'))


class AddTeam(MethodView):
    def get(self):
        return render_template('addTeam.html')

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
        model.insertTeam(sessionID[0],request.form['teamName'])
        return redirect(url_for('dashboard'))
