from flask import request, render_template
from flask.views import MethodView
from flask_cas import login_required
import gbmodel


# A method view class that oversees the viewing of individual student reviews
class ViewReview(MethodView):

    # A function to add a (or some) descriptor word(s) to flush out the numerical ratings we store as answers
    # to most of our review questions
    # INPUT: -self (a reference to the instance of the class the function is being called on?),
    #        -rating (the numerical rating that we will flush out)
    # OUTPUT: a string containing the numerical rating and the descriptor text
    def interperate_rating(self, rating):
        if rating is None:
            return "No Rating Given"
        else:
            interpretation = ""
            if rating == 1:
                interpretation = "Poor"
            elif rating == 2:
                interpretation = "Does Not Meet Expectations"
            elif rating == 3:
                interpretation = "Meets Expectations"
            elif rating == 4:
                interpretation = "Exceeds Expectations"
            elif rating == 5:
                interpretation = "Excellent"
            return str(rating) + " - " + interpretation

    # Prints a given error message to the console and return a rendering of the viewReview.html page with
    # a generic error message in it
    # INPUT: -self,
    #        -error (the error we wil to print to the console)
    # OUTPUT: an error page rendering of the viewReview template
    def handle_error(self, error):
        # We may consider adding logging-
        print(error)
        return render_template('viewReview.html', error="Something went wrong")

    @login_required
    # Determines how the class will handle POST requests
    # INPUT: self
    # OUTPUT: It looks like it will return a rendering of the viewReview.html file. The information included
    #         in this rendering depends on the POST request parameters.
    #         http://flask.pocoo.org/docs/1.0/api/#flask.render_template
    def post(self):
        # Get the database object we will need
        reports = gbmodel.reports()
        teams = gbmodel.teams()
        students = gbmodel.students()

        # Might want some way to verify that the one logged in is a professor
        # Will need an isProf function
        # if not (prof or name == student_name):
        #    error = "You aren't allowed to access this page"
        #    return render_template('errorPage.html', error=error)
        try:
            # Get data from the POST request
            # This helped: https://stackoverflow.com/questions/23205577/python-flask-immutablemultidict
            reviewer_id = request.form.getlist('reviewer_id')[0]
            reviewee_id = request.form.getlist('reviewee_id')[0]
            is_final = int(request.form.getlist('is_final')[0])

            # Query the database for the the reviewing student
            reviewer = students.query.filter_by(id=reviewer_id).first()
            if reviewer is None:
                return self.handle_error("Reviewer not found in the database")

            # Query the database for the student being reviewed
            reviewee = students.query.filter_by(id=reviewee_id).first()
            if reviewee is None:
                return self.handle_error("Reviewee not found in the database")

            # Verify the reviewer and reviewee are are on the same team
            if reviewer.tid != reviewee.tid:
                return self.handle_error("Reviewer and reviewee don't appear to be on the same team")

            # Get the the name of the team the reviewer and reviewee are on
            team_name = teams.get_team_name_from_id(reviewer.tid)
            if team_name is None:
                return self.handle_error("Name of reviewer and reviewee's team not found in database")

            # Finally, get the review and parse it (if we find it in the database)
            report = reports.query.filter_by(reviewer=reviewer_id,
                                             reviewee=reviewee_id,
                                             tid=reviewer.tid,
                                             is_final=is_final).first()
            if report is not None:
                # Get some general report details
                review_details = {"time": report.time,
                                  "reviewer": reviewer.name,
                                  "reviewee": reviewee.name,
                                  "team_name": team_name,
                                  "is_final": (is_final == 1)}

                # Get the main part of the review
                parsed_review = [
                        {"category": "Technical Skill",
                         "content": self.interperate_rating(report.tech_mastery)},
                        {"category": "Work Ethic",
                         "content": self.interperate_rating(report.work_ethic)},
                        {"category": "Communication Skills",
                         "content": self.interperate_rating(report.communication)},
                        {"category": "Cooperation",
                         "content": self.interperate_rating(report.cooperation)},
                        {"category": "Initiative",
                         "content": self.interperate_rating(report.initiative)},
                        {"category": "Team Focus",
                         "content": self.interperate_rating(report.team_focus)},
                        {"category": "Contribution",
                         "content": self.interperate_rating(report.contribution)},
                        {"category": "Leadership",
                         "content": self.interperate_rating(report.leadership)},
                        {"category": "Organization",
                         "content": self.interperate_rating(report.organization)},
                        {"category": "Delegation",
                         "content": self.interperate_rating(report.delegation)},
                        {"category": "Points",
                         "content": report.points},
                        {"category": "Strengths",
                         "content": report.strengths},
                        {"category": "Weaknesses",
                         "content": report.weaknesses},
                        {"category": "Trait work on to become a better team member",
                         "content": report.traits_to_work_on}]

                # Final self reviews will have some extra details
                if reviewer_id == reviewee_id:
                    parsed_review.append({"category": "What the student learned from the experience",
                                          "content": report.what_you_learned})

                    if report.is_final:
                        parsed_review.append({"category": "If the student is proud of their accomplishment",
                                              "content": report.proud_of_accomplishment})

                # Send the data off to the client
                return render_template("viewReview.html", details=review_details, review_data=parsed_review)
            else:
                # Might consider adding more detail so the problem can be addressed more easly
                return self.handle_error("We couldn't find the report we were looking for in the database")

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception as error:
            return self.handle_error(error)
