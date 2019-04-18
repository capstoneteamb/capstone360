"""
from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Dashboard(MethodView):
    def get(self):
        model = gbmodel.get_model()
        students = [dict(name=row[3]) for row in model.selectStudents()]
        return render_template('dashboard.html', students=students)

"""
from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from db_form import db, capstone_session, teams, students, team_members, reports
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import datetime
import gbmodel


#class Dashboard(MethodView):
def get():
    """
    get data from model
    """
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

"""
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
    return lists 
    """

def get_teams():
    return db.session.query(teams)

def get_tid():
    return db.session.query(teams.id).all()

def get_members():
    return db.session.query(students.name, students.tid).filter(students.tid == teams.id)

def choice_query():
    return db.session.query(capstone_session)

class Form(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='start_year', blank_text='Select Term')
