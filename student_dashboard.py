from flask import render_template
from flask.views import MethodView
from catCas import validate_student
from flask_cas import login_required


class StudentDashboard(MethodView):
    @login_required
    def get(self):
        if validate_student() is False:
            return render_template('index.html')
        else:
            student_name = validate_student().name
            user_name = validate_student().id
            return render_template('studentDashboard.html',
                                   name=student_name,
                                   user_name=user_name)
