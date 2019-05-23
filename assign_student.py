from flask import request, render_template
from flask.views import MethodView
import gbmodel
import datetime
from catCas import validate_professor
from flask_cas import login_required

class assignTeam(MethodView):
    @login_required
    def get(self):
        if validate_professor is False:
            msg = "Professor not found"
            return render_template('errorMsg.html', msg=msg)
        session = gbmodel.capstone_session()
        students_table = gbmodel.students()
        team_table = gbmodel.teams()
        # Get session_id from the prefvious selected session
        # If None returned then request for a selection.
        # Otherwise, display the current session_id
        session_id = request.args.get('session_id')
        if session_id is None:
            user_session = request.args.get('selected_session')
            if user_session is not None:
                user_session = user_session.split('-')
                term = str(user_session[0].strip())
                year = int(user_session[1].strip())
            else:
                current_date = datetime.datetime.now()
                month = int(current_date.month)
                year = current_date.year
                if month in range(9, 11):
                    term = "Fall"
                elif month in range(3, 6):
                    term = "Spring"
                elif month in range(6, 9):
                    term = "Summer"
                else:
                    term = "Winter"
            s_id = session.get_session_id(term, year)
            unassigned_students = students_table.get_unassigned_students(s_id)
            sessions = team_table.dashboard(session_id)
            print(s_id)
            return render_template('assignTeam.html', lists=unassigned_students, sessions=sessions, session_id=s_id)
