from flask import render_template
from flask.views import MethodView
from catCas import validate_student
from flask_cas import login_required

# Student Dashboard class handles get requests from index.html
# when student login button is clicked on


class StudentDashboard(MethodView):
    @login_required
    # This method handles get requests to studentDashboard.html
    # Input: only self
    # Output: return to index.html if the student id is not in the student table
    # rendering the studentDashboard.html template
    def get(self):
        if validate_student() is False:
            return render_template('index.html')
        else:
            student_name = validate_student().name
            user_name = validate_student().id
            return render_template('studentDashboard.html',
                                   name=student_name,
                                   user_name=user_name)
