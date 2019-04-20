from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import datetime
import gbmodel

def get():
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

    # What if we don't have any session for this year/term?
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
    
def get_teams():
    return gbmodel.model_sqlalchemy.db.session.query(gbmodel.teams)

def get_members():
    return gbmodel.model_sqlalchemy.db.session.query(gbmodel.students.name, gbmodel.students.tid).filter(gbmodel.students.tid == gbmodel.teams.id)

def choice_query():
    return gbmodel.model_sqlalchemy.db.session.query(gbmodel.capstone_session)

class Form(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='start_year', blank_text='Select Term')
