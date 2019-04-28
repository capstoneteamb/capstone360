from flask import request, render_template
from flask.views import MethodView
import removeDashboard
import gbmodel
import datetime
from flask_cas import login_required


class RemoveStudent(MethodView):
    @login_required
    def get(self):
        return render_template('removeStudent.html')

    def post(self):

        session = gbmodel.capstone_session()
        student = gbmodel.students()

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

        students = request.form.getlist('removedStudent')
        t_name = request.form.get('teamName')
        student.remove_student(students, t_name, session_id)
        lists = removeDashboard.get_rm()
        return render_template('removeDashboard.html', lists=lists)


class RemoveTeam(MethodView):
    @login_required
    def get(self):
        t_name = request.args.get('data')
        t_name = t_name.replace(" ", "_")
        return render_template('removeTeam.html', t_name=t_name)

    def post(self):
        """
        Accepts POST requests and gets the data from the form
        Redirect to index when completed.
        """

        session = gbmodel.capstone_session()
        team = gbmodel.teams()

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

        t_name = request.form.get('teamName')
        t_name = t_name.replace("_", " ")
        team.remove_team(t_name, session_id)
        lists = removeDashboard.get_rm()
        return render_template('removeDashboard.html', lists=lists)
