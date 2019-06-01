from flask import request, render_template
from flask.views import MethodView
from catCas import validate_student
from flask_cas import login_required
import gbmodel
import re


class StudentDashboard(MethodView):
    """
    Student Dashboard class handles get requests from index.html
    when student login button is clicked on
    """
    def valid_email(self, email):
        """
        Verify if the new email is in a correct syntax
        by checking if it has '@' and '.'
        Input: self and new email
        Output: return True if it matches the format, False otherwise
        """
        if len(email) > 7:
            if re.match('^[_a-z0-9-]+(|.[_a-z0-9-]+)*@[a-z0-9-]+'
                        '(|.[a-z0-9-]+)*(|.[a-z]{2,4})$', email) is not None:
                return True
        return False

    @login_required
    def get(self):
        """
        This method handles get requests to studentDashboard.html
        Input: only self
        Output: return to index.html if the student id is not in the student
        table, rendering the studentDashboard.html template
        """
        if validate_student() is False:
            msg = "Student not found"
            return render_template('errorMsg.html', msg=msg, student_register=True)
        else:
            print(validate_student())
            student_name = validate_student().name
            user_name = validate_student().id
            caps = gbmodel.students().get_user_sessions(user_name)  # get user's capstone sessions
            return render_template('studentDashboard.html',
                                   name=student_name,
                                   user_name=user_name,
                                   caps=caps)

    def post(self):
        """
        This method handles post request from editStudent.html
        Input: only self
        Output: prompt to the user error message if the inputs are invalid
                Add new info to the database and return to studentDashboard.html
        """
        student = gbmodel.students()
        student_name = validate_student().name
        user_name = validate_student().id
        new_name = request.form.get('student_new_name')
        new_email = request.form.get('student_new_email')
        caps = gbmodel.students().get_user_sessions(user_name)
        # Only check email validation if new email is entered
        if new_email != '':
            if self.valid_email(str(new_email)) is False:
                error = "Invalid Email Address"
                return render_template('editStudent.html',
                                       error=error,
                                       user_name=user_name)
        student.edit_student(user_name, new_name, new_email)
        # Get new name
        student_name = validate_student().name
        return render_template('studentDashboard.html',
                               name=student_name,
                               user_name=user_name,
                               caps=caps)


class EditStudent(MethodView):
    """
    Edit Student class handles get requests from
    student Dashboard when Edit is clicked on
    """
    @login_required
    def get(self):
        """
        This method handles get request from studentDashboard.html
        Input: only self
        Output: return to editStudent.html
        """
        user_name = validate_student().id
        return render_template('editStudent.html',
                               error=None,
                               user_name=user_name)
