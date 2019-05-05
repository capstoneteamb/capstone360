from flask import request, render_template
from flask.views import MethodView
from flask_cas import login_required
import gbmodel


# Check if a review has been submitted using the given reviewer, reviewee, tid, and is_final variables
# https://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy
def check_review_done(reviews_table, reviewing_student_id, reviewee_student_id, tid, is_final):
    return reviews_table.query.filter_by(reviewer=reviewing_student_id,
                                         reviewee=reviewee_student_id,
                                         tid=tid,
                                         is_final=is_final).first()


# A class for the student page (which allows a professor to click a student and see their reviews)
class ViewStudent(MethodView):
    @login_required
    def post(self):
        # Get the database object we will need
        students = gbmodel.students()
        teams = gbmodel.teams()
        reports = gbmodel.reports()

        # Might want some way to verify that the one logged in is a professor?
        #if not (isProfessor(cas.username)):
        #    error = "You aren't allowed to access this page"
        #    return render_template('errorPage.html', error=error)
        #    *Log Person Out*

        # Otherwise, load the student page
        try:
            # Get the student and session_id from the post request
            student_id = request.form.getlist('student_id')[0]
            session_id = request.form.getlist('session_id')[0]

            # Find the student in the db
            student = students.query.filter_by(id=student_id, session_id=session_id).first()

            # If the student is found, find all of the student's team members and see if the student filled
            # out reviews for them
            if student is not None:
                # Get team name and record it and the student's name (these will be displayed on the page)
                team_name = teams.get_team_name_from_id(student.tid)[0]
                student_details = {"name": student.name, "id": student.id, "team_name": team_name}

                # This will hold midterm and final reviews
                reviews = []

                # See if the student completed a midterm and final review for their team members and
                # record it
                team_members = students.query.filter_by(tid=student.tid, session_id=session_id).all()
                for team_member in team_members:
                    midterm_review_completed = check_review_done(reports, student.id, team_member.id,
                                                                 student.tid, False)
                    final_review_completed = check_review_done(reports, student.id, team_member.id,
                                                               student.tid, True)
                    reviews.append({"reviewee_name": team_member.name,
                                    "reviewee_id": team_member.id,
                                    "completed": (midterm_review_completed, final_review_completed)})

                # Combine the recorded data with the viewStudent.html template and render the viewStudent
                # page
                return render_template('viewStudent.html', student=student_details, review_data=reviews)
            else:
                error = "We couldn't find this student in the database?"
                return render_template('viewStudent.html', error=error)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception:
            error = "Something went wrong :("
            return render_template('viewStudent.html', error=error)
