from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime

class RemoveDashboard(MethodView):
    def get(self):
        """
        get data from model
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
        
        tids = [row[0] for row in model.getTeam_sessionID(sessionID[0])]
        teamNames = [row[2] for row in model.getTeam_sessionID(sessionID[0])]
        lists = [[] for _ in range(len(tids))]
       
        for i in range(len(tids)):
            students = model.getStudents(tids[i], sessionID[0])
            temp = [ teamNames[i]]
            for student in students:
                temp.append(student[0])
            lists[i] = temp
        return render_template('removeDashboard.html', lists = lists)

