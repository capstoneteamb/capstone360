from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
import dashboard

# A class for the student page (it allows a professor to click a student and see a list of all of their reports)
class ViewStudent(MethodView):
    def post(self):
        # Get id and query database for their information
        # Get the student's name (will be displayed) and potentially team number -- might be a nice feature
        # Get Will need to check for midterm and final reviews and create some way to display them. May consider creating a review page
        # Will need to get their reports, once those are created, and display those as well
        #student = gbmodel.student().query()
        #reviews = gbmodel.reviews().query()
        #teams = gbmodel.teams().query()

        # Get the database object we will need
        session = gbmodel.capstone_session()
        students = gbmodel.students()
        teams = gbmodel.teams()
        reports = gbmodel.reports()

        # Get the active session
        # Consider all of this to a function (this might allow some other way to make session viewable)
        # May need a get session function
        """currentDate = datetime.datetime.now()
        month = int(currentDate.month) 
        year = currentDate.year
        if month in range (9, 11):   term = "Fall"
        elif month in range (3,5):   term = "Spring"
        elif month in range (6,8):   term = "Summer"
        else:                        term = "Winter"
        session_id = session.get_session_id(term, year)"""

        # Get some things we will need from the post request
        #session_id = request.form.getlist('session_id')[1]
        print(request.form)
        team_id = request.form.getlist('team_id')[0]
        student_name = request.form.getlist('student_name')[0]
        session_id = request.form.getlist('session_id')[0]

        # We will need some way to verify that the one logged in is a professor
        # Will need an isProf function
        #if not (prof or name == student_name):
        #    error = "You aren't allowed to access this page"
        #    return render_template('errorPage.html', error=error)
        
        # Otherwise, load the student page
        try:
            # Make sure the student exists before we try to load anything
            student = students.get_student_from_name_and_tid(student_name, team_id)

            if student is not None:
                # Get team name and construct student information construct
                team_name = teams.get_team_name_from_id(student.tid)[0]
                student_details = {"name": student.name, "team": team_name, "tid": student.tid, "session_id": session_id}

                # Will hold midterm and final reviews
                reviews = []
                
                # See if the student completed a midterm and final review for their team members and
                # record it
                team_members = students.get_students_info(student.tid, session_id)
                for team_member in team_members:
                    midterm_review_completed = reports.check_report_submitted_for_student(student.tid, student.id, team_member.id, False)
                    final_review_completed = reports.check_report_submitted_for_student(student.tid, student.id, team_member.id, True)
                    reviews.append({"reviewee_name": team_member.name, "midterm_completed": midterm_review_completed, "final_completed": final_review_completed})
                    
                # Send the recorded data over to the student page and render it
                return render_template('student.html', student = student_details, review_data = reviews)

            else:
                error = "There was a problem"
                return render_template('student.html', error = error)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            #error = "Something went wrong :("
            return render_template('student.html', error = error)
