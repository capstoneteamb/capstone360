from flask import redirect, render_template, request, g, url_for
from flask.views import MethodView
import os
import gbmodel
import datetime
import csv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
class CreateTeam(MethodView): # Was orignally called addTeam, name was changed due to another member having this name in the master branch
  def get(self):
    return render_template('profAddTeam.html')
  def post(self):
    session = gbmodel.capstone_session()
    teams = gbmodel.teams() # Accessor to the teams table
    students_table = gbmodel.students() # Accessor to the students table
    team_name = request.form['Team Name']
    #Let s represent a single student
    s1 = request.form['student1']
    s2 = request.form['student2']
    s3 = request.form['student3']
    s4 = request.form['student4']
    s5 = request.form['student5']
    s6 = request.form['student6']
    s7 = request.form['student7']
    s8 = request.form['student8']
    students = [s1, s2, s3, s4, s5, s6, s7, s8] # An array containing all students
    # Get date to determine session id
    current_date = datetime.datetime.now()
    month = int(current_date.month) 
    year = current_date.year
    if month in range (9, 11):   term = "Fall"
    elif month in range (3,5):   term = "Spring"
    elif month in range (6,8):   term = "Summer"
    else:                        term = "Winter"
    sessionID = session.getSessionID(term, year)
    teams.insertTeam(sessionID, team_name)
    for s in students: # For loop that updates all students TID to their new teams TID
      students_table.updateTeam(s, sessionID)
    return render_template('profAddTeam.html')

