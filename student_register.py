from flask import request, render_template
from flask.views import MethodView
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
        logging.error("Student Register Failure: " + str(console_error))
        return render_template("studentRegister.html", message=user_error, is_error=True)

    @login_required
    def get(self):
        """
        Determines how the Student Register class handles GET requests. It loads a page that a student can
        fill out and submit to register for a selected capstone_session
        Input: self
        Output: a rendering of the view student page
        """
        # Get the currently active sessions
        parsed_sessions = []
        active_sessions = gbmodel.capstone_session().get_active_sessions()
        if active_sessions is None:
            return self.handle_error("No active sessions to register for",
                                     "No active capstone sessions to register for")
        for session in active_sessions:
            parsed_sessions.append({"id": session.id,
                                    "term": session.start_term + " " + str(session.start_year)})

        # Render the template
        return render_template('studentRegister.html', sessions=parsed_sessions)

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
        teams = gbmodel.teams()

        # Otherwise, load the student page
        try:
            # Get the student_id and information the student submitted via the form
            student_id = CAS().username
            name = request.form.getlist('name')[0]
            email_address = request.form.getlist('email_address')[0]
            session_id = request.form.getlist('session_id')[0]

            # Verify that the student isn't already registered for the target session
            if students.get_student_in_session(student_id, session_id) is not None:
                return self.handle_error("Student already registered for target session",
                                         "You already registered for this session")

            # Add the student to the database
            # The student won't be on a team when they first sign up, so we have to assign them to the
            # empty team for the target session. We start by checking if the empty team exists. If the
            # target session doesn't have one yet, we create it
            if teams.get_team_from_name("", session_id) is None:
                teams.insert_team(session_id, "")

            # Insert the student into the database (as a part of the empty team)
            students.insert_student(name, email_address, student_id, session_id, "")

            # Log the event and render the page with a message telling the student that they have been
            # registered (along with a link to the student page)
            logging.info("Student Registered For Capstone Session")
            return render_template('studentRegister.html', message="Successfully registered!", is_error=False)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            return self.handle_error(error, "Something went wrong")
