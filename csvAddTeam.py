from flask import render_template, request
from flask.views import MethodView
from flask_cas import login_required
from sqlalchemy.exc import SQLAlchemyError
import gbmodel
import datetime
import csv
import io


class AddTeamCSV(MethodView):
    @login_required
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
            if month in range(9, 11):
                term = "Fall"
            elif month in range(3, 5):
                term = "Spring"
            elif month in range(6, 8):
                term = "Summer"
            else:
                term = "Winter"

            session_id = session.get_session_id(term, year)
            # Create team if it doesn't exist, then create the student.
            try:
                if teams_table.check_dup_team(team_name, session_id) is True:
                    teams_table.insert_team(session_id, team_name)
            except SQLAlchemyError:
                self.display_error('team table error')
            try:
                students_table.insert_student(student_name,
                                              "", student_id,
                                              session_id, team_name)
            except SQLAlchemyError:
                self.display_error('Error inserting student into\
                                   students table.')
        return render_template('csvAddTeam.html')
