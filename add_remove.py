from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime

class Dashboard(MethodView):
    def get(self):
        """
        get data from model
        """
        session = gbmodel.capstone_session()
        team = gbmodel.teams()
        student = gbmodel.students()
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
                if month in range (9, 11):   term = "Fall"
                elif month in range (3,5):   term = "Spring"
                elif month in range (6,8):   term = "Summer"
                else:                        term = "Winter"

            sessionID = session.getSessionID(term, year)
    
        tids = [row[0] for row in team.getTeam_sessionID(sessionID)]
        teamNames = [row[2] for row in team.getTeam_sessionID(sessionID)]
        lists = [[] for _ in range(len(tids))]
        
        for i in range(len(tids)):
            names = student.getStudents(tids[i], sessionID)
            temp = [teamNames[i]]
            for name in names:
                temp.append(name[0])
            lists[i] = temp
        sessions = session.getSessions()
       
        return render_template('dashboard.html', lists = lists, sessions=sessions, sessionID=sessionID)

    def post(self):

        student = gbmodel.students()
        team = gbmodel.teams()       
        sessionID = request.form['sessionID']
        sessionID = int(sessionID[0])
        if 'studentName' in request.form:
            while not student.checkDupStudent(request.form['studentID'], sessionID):
                error = "Student id "+ str(request.form['studentID']) + " already exists"
                return render_template('addStudent.html', tName = teamName, error=error)
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")
            student.insertStudent(request.form['studentName'], request.form['studentID'], sessionID, tName)  
            lists, sessions = team.dashboard(sessionID)       
            return render_template('dashboard.html', lists = lists, sessions=sessions, sessionID=sessionID)

        elif 'removedStudent' in request.form:
            students = request.form.getlist('removedStudent')  
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")   
            student.removeStudent(students, tName, sessionID)
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists = lists, sessions=sessions, sessionID=sessionID)  

        elif 'removeTeam' in request.form:
            teamName = request.form.get('removeTeam')
            tName = teamName.replace("_", " ")
            print("remove team:", tName)
            team.removeTeam(tName, sessionID)
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists = lists, sessions=sessions, sessionID=sessionID)   

        elif 'teamName' in request.form:   
            while not team.checkDupTeam(request.form['teamName'], sessionID):
                error = "Team name already exists"
                return render_template('addTeam.html', error=error)
            teamName = request.form.get('teamName')
            tName = teamName.replace("_", " ")
            team.insertTeam(sessionID, teamName)      
            lists, sessions = team.dashboard(sessionID)
            return render_template('dashboard.html', lists = lists, sessions=sessions, sessionID=sessionID)      

class AddStudent(MethodView):
    def get(self):
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        sessionID = request.args.get('sessionID')
        return render_template('addStudent.html', tName = str(tName), sessionID = sessionID, error=None)


class AddTeam(MethodView):
    def get(self):
        error = None
        sessionID = request.args.get('sessionID')
        return render_template('addTeam.html', error=error, sessionID=sessionID)

class RemoveTeam(MethodView):
    def get(self):
        tName = request.args.get('data')
        tName = tName.replace(" ", "_")
        sessionID = request.args.get('sessionID')
        print("session from remove team", sessionID)
        return render_template('removeTeam.html', tName = tName, sessionID=sessionID)
