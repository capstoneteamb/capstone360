from flask import request, render_template
from flask.views import MethodView
from flask_cas import login_required, CAS
import gbmodel
import logging


class StudentRegister(MethodView):
    """
    Facilitates the rendering and processing of the register student page, which allows students to register
    for a currently ongoing Capstone session
    """

    def display_error(self, error_msg):
        """
        Returns an error-page rendering of studentRegister.html that displays the given error_msg
        Input: self, error_msg
        Output: the error-page rendering of the studentRegister.html template
        """
        return render_template("studentRegister.html", message=error_msg, is_error=True)

    @login_required
    def get(self):
        """
        Processes student register class GET requests. More specifically, it loads a form that a student (once
        logged in) can fill out and submit in order to register for an active Capstone session.
        Input: self
        Output: a rendering of the student register page: featuring a student registration form if everything
                went well, or an error message if something went wrong
        """

        # Get the database objects we will need
        capstone_session = gbmodel.capstone_session()
        professors = gbmodel.professors()

        # Get the currently active Capstone sessions
        sessions = capstone_session.get_active_sessions()
        if sessions is None:
            # https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
            # (discovered via: https://docs.python-guide.org/writing/logging/)
            logging.warning(("A student tried to register for a Capstone session, but no active sessions "
                             "were available"))
            return self.display_error("There aren't any active Capstone sessions to register for")

        # Build a list containing the id and a descriptor string of the active sessions
        active_sessions = []
        for session in sessions:
            # Get the name of the professor running the session
            professor = professors.get_professor(session.professor_id)
            if professor is None:
                logging.error(("Student Registration Failure - the professor of a specific Capstone session "
                               "wasn't found. Was the professor removed from the database?"))
                return self.display_error("Something went wrong")

            # Create the data structure entry
            active_sessions.append({"id": session.id,
                                    "descriptor": "{} {} - {}".format(session.start_term,
                                                                      str(session.start_year),
                                                                      professor.name)})

        # Render the studentRegister template using the list we put together
        return render_template('studentRegister.html', sessions=active_sessions)

    @login_required
    def post(self):
        """
        Handles student registration requests, which come in the form of POST requests submitted via the form
        that is generated in GET requests
        Input: self
        Output: a rendering of the student register page: with a success message and link to the student
                dashboard if everything went well, or with an error message if there was a problem
        """
        # Get the database objects we will need
        students = gbmodel.students()
        teams = gbmodel.teams()

        # Continue processing the POST request
        try:
            # Get the student_id and information the student submitted via the form
            student_id = CAS().username
            name = request.form.getlist('name')[0]
            email_address = request.form.getlist('email_address')[0]
            session_id = request.form.getlist('session_id')[0]

            # Verify that the student isn't already registered for the target session
            if students.get_student_in_session(student_id, session_id) is not None:
                logging.warning(("A student tried to register for a Capstone session, but the student was "
                                 "already registered for the session"))
                return self.display_error("You are already in this session")

            # Add the student to the database
            # The student won't be on a team when they first sign up, so we have to assign them to the
            # empty team for the target session. We start by checking if the empty team exists. If the
            # target session doesn't have one yet, we create it
            if teams.get_tid_from_name("", session_id) is None:
                teams.insert_team(session_id, "")

            # Insert the student into the database (as a part of the empty team)
            students.insert_student(name, email_address, student_id, session_id, "")

            # Log the event and render the page with a message telling the student that they have been
            # registered (along with a link to the student page)
            logging.info("A student registered for a Capstone session")
            return render_template('studentRegister.html', message="Successfully registered!", is_error=False)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            logging.error("Student Registration Failure: " + str(error))
            return self.display_error("Something went wrong")
