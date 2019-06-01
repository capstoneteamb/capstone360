from flask import request, render_template
from flask.views import MethodView
from flask_cas import login_required
from catCas import validate_professor
import gbmodel
import logging

"""
A class for the student page (that a professor would access form the professor dashboard. The professor
should be able to use this page to access the midterm and final reviews for a student)
"""


class ViewStudent(MethodView):

    def check_review_done(self, reviews_table, reviewer_id, reviewee_id, team_id, is_final):
        """
        Check if a review has been submitted using the given reviewer, reviewee, team_id, and is_final
        INPUT: -self,
               -reviews_table (an instance of gbmodel.reports() class that we use to make our database call),
               -reviewer_id (the id of the student who authored the review we are looking for),
               -reviewee_id (the id of the student being reviewed),
               -team_id (the id of the team the reviewer and reviewee are on),
               -is_final (a boolean to indicate if we are looking for a midterm or final review)
        OUTPUT: a boolean indiating if the review was found in the database or not
        """
        return reviews_table.get_report(reviewer_id, reviewee_id, team_id, is_final) is not None

    def display_error(self, error):
        """
        Prints a given error message to the console and returns a rendering (?) of the viewStudent template
        with a generic error message in it
        INPUT: -self,
               -error (the error we wil to print to the console)
        OUTPUT: an error page rendering of the viewStudent template (I think)
        """
        logging.error("View Student - " + str(error))
        return render_template('viewStudent.html', error="Something went wrong")

    @login_required
    def post(self):
        """
        A function that determines how the viewStudent class handles POST requests
        INPUT: self
        OUTPUT: a rendering of the viewStudent.html file. The information included in the rendering depends on
                the information we get from the POST request
        """
        # Get the database object we will need
        students = gbmodel.students()
        teams = gbmodel.teams()
        reports = gbmodel.reports()

        # Validate that the one making the request is a professor
        # Might want to consider noting things like these or forcefuly logging the person out
        if not validate_professor():
            return self.display_error(("A student (or someone else) tried to access the view_student page (a "
                                       "page that professors should only have access to)"))

        # Otherwise, load the student page
        try:
            # Get the student and session id from the post request, and try to find the student in the db
            student_id = request.form.getlist('student_id')[0]
            session_id = request.form.getlist('session_id')[0]
            student = students.get_student_in_session(student_id, session_id)

            # If the student is found, find all of the student's team members and see if the student filled
            # out reviews for those team members
            if student is not None:
                # Get team name
                team = teams.get_team_from_id(student.tid)
                if team is None:
                    return self.display_error(("Students' team not found in database (when searching via team"
                                               " id)"))

                # Record it, along with some other information about the student
                student_details = {"name": student.name, 
                                   "id": student.id,
                                   "team_name": team.name}

                # See if the student completed a midterm and final review for their team members and
                # record it
                reviews = []
                team_members = students.get_team_members(student.tid)
                for team_member in team_members:
                    midterm_review_completed = self.check_review_done(reports,
                                                                      student.id,
                                                                      team_member.id,
                                                                      student.tid,
                                                                      False)
                    final_review_completed = self.check_review_done(reports,
                                                                    student.id,
                                                                    team_member.id,
                                                                    student.tid,
                                                                    True)
                    reviews.append({"reviewee_name": team_member.name,
                                    "reviewee_id": team_member.id,
                                    "completed": (midterm_review_completed, final_review_completed)})

                # Combine the recorded data with the viewStudent.html template and render the viewStudent
                # page
                return render_template('viewStudent.html',
                                       student=student_details,
                                       review_data=reviews,
                                       session_id=session_id)
            else:
                return self.display_error(("Student was not found in the database "
                                           "(when we searched via student ID)"))

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            return self.display_error(error)
