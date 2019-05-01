from flask import request, render_template
from flask.views import MethodView
import gbmodel


# A class for the student page (which allows a professor to click a student and see their reviews)
class ViewStudent(MethodView):
    def post(self):
        # Get the database object we will need
        students = gbmodel.students()
        teams = gbmodel.teams()
        reports = gbmodel.reports()

        # Get some things we will need from the post request
        team_id = request.form.getlist('team_id')[0]
        student_name = request.form.getlist('student_name')[0]
        session_id = request.form.getlist('session_id')[0]

        # We will need some way to verify that the one logged in is a professor
        # Will need an isProf function
        # if not (prof or name == student_name):
        #    error = "You aren't allowed to access this page"
        #    return render_template('errorPage.html', error=error)

        # Otherwise, load the student page
        try:
            # Make sure the student exists before we try to load anything
            student = students.get_student_from_name_and_tid(student_name, team_id)

            if student is not None:
                # Get team name and construct student information construct
                team_name = teams.get_team_name_from_id(student.tid)[0]
                student_details = {"name": student.name,
                                   "team": team_name,
                                   "tid": student.tid,
                                   "session_id": session_id}

                # Will hold midterm and final reviews
                reviews = []

                # See if the student completed a midterm and final review for their team members and
                # record it
                team_members = students.get_students_info(student.tid, session_id)
                for team_member in team_members:
                    midterm_review_completed = reports.check_report_submitted(student.tid, student.id,
                                                                              team_member.id, False)
                    final_review_completed = reports.check_report_submitted(student.tid, student.id,
                                                                            team_member.id, True)
                    reviews.append({"reviewee_name": team_member.name,
                                    "completed": (midterm_review_completed, final_review_completed)})

                # Send the recorded data over to the student page and render it
                return render_template('viewStudent.html', student=student_details, review_data=reviews)

            else:
                error = "There was a problem"
                return render_template('viewStudent.html', error=error)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            error = "Something went wrong :("
            return render_template('viewStudent.html', error=error)
