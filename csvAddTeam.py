from flask import redirect, render_template, request, g, url_for
from flask.views import MethodView
import gbmodel
import datetime
import csv
import io
import os


class AddTeamCSV(MethodView):
    def get(self):
        return render_template('csvAddTeam.html')
    def post(self):
        session = gbmodel.capstone_session()
        teams_table = gbmodel.teams()  # Accessor to the teams table
        students_table = gbmodel.students()  # Accessor to the students table
        file = request.files['teamcsv']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream, delimiter=',')
        for row in csv_reader:
            student_name = row[0]
            student_id = row[1]
            team_name = row[2]

            # Get date to determine session ID
            current_date = datetime.datetime.now()
            month = int(current_date.month) 
            year = current_date.year
            if month in range(9, 11):   term = "Fall"
            elif month in range(3, 5):   term = "Spring"
            elif month in range(6, 8):   term = "Summer"
            else:                        term = "Winter"
            session_id = session.get_session_id(term, year)
            # Create team if it doesn't exist, then create the student.
            if teams_table.check_dup_team(team_name, session_id) == True:
                teams_table.insert_team(session_id, team_name)
            students_table.insert_student(student_name, "", student_id, session_id, team_name)
        return render_template('csvAddTeam.html')
