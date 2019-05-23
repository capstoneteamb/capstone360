from flask import render_template, request
from flask.views import MethodView
from flask_cas import login_required
from sqlalchemy.exc import SQLAlchemyError
import gbmodel
import datetime
import csv
import io

# Create a webpage for professors to import students
# via csv file.
class AddTeamCSV(MethodView):
    @login_required
    # Display webpage
    # INPUT: Session id from the professor dashboard.
    # OUTPUT: 
    def get(self):
        session_id = request.args.get('session_id')
        return render_template('csvAddTeam.html', session_id=session_id)

    def post(self):
        session_id = request.form['session_id']
        session_id = int(session_id)
        teams_table = gbmodel.teams()  # Accessor to the teams table
        students_table = gbmodel.students()  # Accessor to the students table
        file = request.files['teamcsv']
        # If 'Create from File' was selected with no file
        # return back to import student page.
        if(file.filename == ''):
            return render_template('csvAddTeam.html', session_id=session_id)
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream, delimiter=',')
        for row in csv_reader:
            student_name = row[0]
            student_id = row[1]
            team_name = row[2]

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
        return render_template('csvAddTeam.html', session_id=session_id)
