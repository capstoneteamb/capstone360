from flask import request, render_template
from flask.views import MethodView
from catCas import validate_student
from flask_cas import login_required, CAS
import gbmodel
import logging

class StudentRegister(MethodView):
    """
    Facilitates the rendering and processing of the register student page, which allows students to register
    for a currently ongoing capstone session
    """
    
    def handle_error(self, console_error, user_error=None):
        """
        Handles errors (print the error message to the console and return an error page to the user
        Input: self, console_error (the error message to be printed to the console or be logged), user_error
               (an error message to be displayed to the user, if given. If not given, the user will see the
               console_error message)
        Output: an error page version of the studentRegister.html template
        """

        if user_error is None:
            user_error = console_error

        # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
        # (discovered via: https://docs.python-guide.org/writing/logging/)
        logging.error("Student Register Failure: " + console_error)
        return render_template("studentRegister.html", message=user_error, is_error=True)


    @login_required
    def get(self):
        """
        Determines how the Student Register class handles GET requests. It loads a page that the a student
        can fill out and submit to register for a selected capstone_session
        Input: self
        Output: a rendering of the view student page
        """
        # Get the student id from the request and, if it's there, build the register page
        student_id = CAS().username

        # Get the currently active sessions
        capstone_session = gbmodel.capstone_session()
        active_sessions = capstone_session.get_active_sessions()
        if active_sessions is None:
            return self.handle_error("No active sessions to register for",
                                     "No active capstone sessions to register for")

        parsed_sessions = [] # Maybe move somewhere else
        for session in active_sessions:
            parsed_sessions.append({"id": session.id, "term": session.start_term + " " + str(session.start_year)})

        # Render the template
        return render_template('studentRegister.html', sessions=parsed_sessions)


    # A function that determines how the viewStudent class handles POST requests
    # INPUT: self
    # OUTPUT: a rendering of the viewStudent.html file. The information included in the rendering depends on
    #         the information we get from the POST request
    @login_required
    def post(self):
        """
        Determines how the Student Register class handles POST requests. It processes student register
        requests so that they can be added to the class, then loads the student register page with a
        message telling them that they have been successfully added to the course (and give them a link to
        get to the student page
        Input: self
        Output: the studentRegister page, with a success message and link, or an error message
        """
        # Get the database object we will need
        students = gbmodel.students()

        # Otherwise, load the student page
        try:
            # Get the student and session id from the post request, and try to find the student in the db
            student_id = CAS().username
            name = request.form.getlist('name')[0]
            email_address = request.form.getlist('email_address')[0]
            session_id = request.form.getlist('session_id')[0]

            # Verify that the student isn't already registered in the current session
            if students.get_student_in_session(student_id, session_id) is not None:
                return self.handle_error("Student already registered for target session",
                                         "You already registered for this session")

            # Add the student to the database
            students.insert_student(name, email_address, student_id, session_id, None)

            # Log the event and render the page with a message telling the student that they have been
            # registered (along with a link to the student page)
            logging.info("Student Registered For Capstone Session")
            return render_template('studentRegister.html', message="Successfully registered!", is_error=False)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            return self.handle_error(error, "Something went wrong")
