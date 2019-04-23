from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime


def get_rm():
    currentDate = datetime.datetime.now()
    month = int(currentDate.month)
    
    year = currentDate.year
    if month in range (9, 11):   term = "Fall"
    elif month in range (3,5):   term = "Spring"
    elif month in range (6,8):   term = "Summer"
    else:                        term = "Winter"
    session = gbmodel.capstone_session()
    team = gbmodel.teams()
    student = gbmodel.students()

    sessionID = session.getSessionID(term, year)
    tids = [row[0] for row in team.get_team_session_id(sessionID)]
    teamNames = [row[2] for row in team.get_team_session_id(sessionID)]
    lists = [[] for _ in range(len(tids))]
    
    for i in range(len(tids)):
        names = student.get_students(tids[i], sessionID)
        temp = [teamNames[i]]
        for name in names:
            temp.append(name[0])
        lists[i] = temp
    return lists 
    

