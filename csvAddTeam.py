from flask import redirect, render_template, request, g, url_for
from flask.views import MethodView
import os
import gbmodel
import datetime
import csv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import io
class csvAddTeam(MethodView):
  def get(self):
    return render_template('csvAddTeam.html')
  def post(self):
    session = gbmodel.capstone_session()
    teams_table = gbmodel.teams() # Accessor to the teams table
    students_table = gbmodel.students() # Accessor to the students table
    file = request.files['teamcsv']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.reader(stream, delimiter=',')
    for row in csv_reader:
      team_name = row[0]
      students = []
      i = 1 # Incrementor for while loop below
      while i < len(row):
        students.extend([row[i]])
        i+=1
      # Get date to determine session ID
      current_date = datetime.datetime.now()
      month = int(current_date.month) 
      year = current_date.year
      if month in range (9, 11):   term = "Fall"
      elif month in range (3,5):   term = "Spring"
      elif month in range (6,8):   term = "Summer"
      else:                        term = "Winter"
      sessionID = session.getSessionID(term, year)
      teams_table.insertTeam(sessionID, team_name) # Insert the new team to the DB
      for s in students:
        students_table.updateTeam(s, sessionID)
      return render_template('csvAddTeam.html')
