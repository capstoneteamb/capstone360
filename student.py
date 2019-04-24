from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
import dashboard

class ViewStudent(MethodView):
    def get(self):
        # Get information of logged in student or from post
        #tName = request.args.get('student')

        # Get id and query database for their information
        # Get the student's name (will be displayed) and potentially team number -- might be a nice feature
        # Get Will need to check for midterm and final reviews and create some way to display them. May consider creating a review page
        # Will need to get their reports, once those are created, and display those as well
        #student = gbmodel.student().query()
        #reviews = gbmodel.reviews().query()
        #teams = gbmodel.teams().query()

        #student_id = query
        #tName = tName.replace(" ", "_")

        return render_template('student.html')

    #def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """
"""
        # Get the database object we will need
        session = gbmodel.capstone_session()
        student = gbmodel.students()

        # Get the active session
        # Consider all of this to a function (this might allow some other way to make session viewable)
        currentDate = datetime.datetime.now()
        month = int(currentDate.month) 
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"
        session_iD = session.getSessionID(term, year)

        # Get the student name
        student_name = request.form.get('studentName')

        # We will need some way to verify that the one logged in is a professor
        if not (prof or name == student_name):
            error = "You aren't allowed to access this page"
            return render_template('errorPage.html', error=error)
        
        # Otherwise, load the student page
        try:
            # Make sure the student exists before we try to load anything
            if student.getStudent(student_name, session_id):
                # Get Team Name

                
                # Check if midterm review is completed
                midterm_review_completed = False

                # Check if final review is completed
                final_review_completed = False

                # Check if midterm report is created
                midterm_report_created = False

                # check if final report is created
                final_report_created = False

                # Return the student page
                completed_items = {'midterm': (midterm_review_completed, final_review_completed),
                             'final': (midterm_report_created, final_report_created)}
                return render_template('student.html', name = student_name, completed = completed_items)
            else:
                error = "student not found"
                return render_template('error.html', error=error)
        except():
            return None"""


"""
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
        return render_template('addTeam.html', error=error)"""
