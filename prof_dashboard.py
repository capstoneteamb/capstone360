from flask import redirect, request, url_for, render_template
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

        # Get sessionID from the prefvious selected session
        # If None returned then request for a selection.
        # Otherwise, display the current sessionID

        sessionID = request.args.get('sessionID')

        if sessionID is None:
            user_session = request.args.get('selected_session')

            if user_session is not None:
                user_session = user_session.split('-')
                term = str(user_session[0].strip())
                year = int(user_session[1].strip())

            else:
                currentDate = datetime.datetime.now()
                month = int(currentDate.month)       
                year = currentDate.year
                if month in range(9, 11):
                    term = "Fall"
                elif month in range(3, 5):
                    term = "Spring"
                elif month in range(6, 8):
                    term = "Summer"
                else:
                    term = "Winter"

            sessionID = session.get_session_id(term, year)

        # Lists - a list of teams and students of a selected session to display on the dashboard
        # Sessions - a list of sessions to display in drop downs
        lists, sessions = team.dashboard(sessionID)

        return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID)

    def post(self):
        session = gbmodel.capstone_session()
        student = gbmodel.students()
        team = gbmodel.teams()       
        sessionID = request.form['sessionID']
        sessionID = int(sessionID[0])

        # If ADD STUDENT form was submitted (addStudent)
        if 'studentName' in request.form:
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")
            while not student.check_dup_student(request.form['studentID'], sessionID):
                error = "Student id " + str(request.form['studentID']) + " already exists"
                return render_template('addStudent.html', tName=teamName, sessionID=sessionID, error=error)         
            student.insert_student(request.form['studentName'], request.form['studentID'], sessionID, tName)  
            lists, sessions = team.dashboard(sessionID)       
            return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID)

        # If REMOVE STUDENT was submitted (in dashboard)
        elif 'removedStudent' in request.form:
            students = request.form.getlist('removedStudent')  
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")   
            student.remove_student(students, tName, sessionID)
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID)  

        # If REMOVE TEAM was submitted (removeTeam)
        elif 'removeTeam' in request.form:
            teamName = request.form.get('removeTeam')
            tName = teamName.replace("_", " ")
            team.remove_team(tName, sessionID)
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID)   

        # If ADD TEAM was submitted (addTeam)
        elif 'teamName' in request.form:   
            while not team.check_dup_team(request.form['teamName'], sessionID):
                error = "Team name already exists"
                return render_template('addTeam.html', error=error, sessionID=sessionID)
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")
            team.insert_team(sessionID, teamName)      
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID)   

        # If SET DATE for reviews was submitted (setDate)  
        elif 'midtermStart' in request.form:
            midtermStart = request.form.get('midtermStart')
            midtermEnd = request.form.get('midtermEnd')
            finalStart = request.form.get('finalStart')
            finalEnd = request.form.get('finalEnd')
            # params = {'mStart': midtermStart, 'mEnd': midtermEnd, 'fStart': finalStart, 'fEnd': finalEnd}

            session.insert_dates(midtermStart, midtermEnd, finalStart, finalEnd, sessionID)
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists=lists, sessions=sessions, sessionID=sessionID) 


class AddStudent(MethodView):
    @login_required
    def get(self):
        # Get team_id, team name and session id from dashboard
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        sessionID = request.args.get('sessionID')
        return render_template('addStudent.html', tName=str(tName), sessionID=sessionID, error=None)


class AddTeam(MethodView):
    @login_required
    def get(self):
        # Get seesion id from dashboard
        sessionID = request.args.get('sessionID')
        return render_template('addTeam.html', error=None, sessionID=sessionID)


class RemoveTeam(MethodView):
    @login_required
    def get(self):
        # Get team name, the spaces were replaced with '_' in order to keep the entire name.
        # Otherwise the part after spaces would be cut (for some reason)
        # Also, Get session id from dashboard
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        sessionID = request.args.get('sessionID')
        return render_template('removeTeam.html', tName=tName, sessionID=sessionID)


class SetDate(MethodView):
    @login_required
    def get(self):
        sessionID = request.args.get('sessionID')
        return render_template('setDate.html', sessionID=sessionID)
