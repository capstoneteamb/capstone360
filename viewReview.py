from flask import request, render_template
from flask.views import MethodView
from flask_cas import login_required
import gbmodel


# A function to add some descriptor words to flush out our numerical rating system a little bit
def interperate_rating(rating):
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


# A method view class that facillitates the seeing of individual student reviews
# We might need to start thinking about security
class ViewReview(MethodView):
    @login_required
    def post(self):
        # Get the database object we will need
        reports = gbmodel.reports()
        teams = gbmodel.teams()
        students = gbmodel.students()

        # Get data from the POST request
        # This helped: https://stackoverflow.com/questions/23205577/python-flask-immutablemultidict
        reviewer_name = request.form.getlist('reviewer_name')[0]
        reviewee_name = request.form.getlist('reviewee_name')[0]
        team_id = request.form.getlist('tid')[0]
        try:
            is_final = int(request.form.getlist('is_final')[0])
        except ValueError:
            print("Error converting is_final to int in viewReview.py")
            error = "Something went wrong"
            return render_template('viewReview.html', error=error)

        # We will need some way to verify that the one logged in is a professor
        # Will need an isProf function
        # if not (prof or name == student_name):
        #    error = "You aren't allowed to access this page"
        #    return render_template('errorPage.html', error=error)

        # Get student_ids from name
        reviewer_id = students.get_student_from_name_and_tid(reviewer_name, team_id).id
        reviewee_id = students.get_student_from_name_and_tid(reviewee_name, team_id).id

        # Otherwise, load the review page
        try:
            # Get Team name
            team_name = teams.get_team_name_from_id(team_id)[0]

            # Get report data and, if the report is there, parse it
            report = reports.query.filter_by(reviewer=reviewer_id,
                                             reviewee=reviewee_id,
                                             tid=team_id,
                                             is_final=is_final).first()
            if report is not None:
                review_details = {"time": report.time,
                                  "reviewer": reviewer_name,
                                  "reviewee": reviewee_name,
                                  "team_name": team_name,
                                  "is_final": (is_final == 1)}
                parsed_review = [
                        {"question": ("[Technical Skill] Mastery of the skills involved in their role(s) with"
                                      " the project. This may be programming, database design, management,"
                                      " requirements elicitation, etc"),
                         "answer": interperate_rating(report.tech_mastery)},
                        {"question": ("[Work Ethic] Cheerfully performing their tasks without excessive"
                                      " complaining, work avoidance, etc"),
                         "answer": interperate_rating(report.work_ethic)},
                        {"question": ("[Communication Skills] Ability to understand others' points and to"
                                      " effectively get their points across"),
                         "answer": interperate_rating(report.communication)},
                        {"question": ("[Cooperation] Willing to be flexible, share knowledge & genuinely"
                                      " interested in what they can do to make the project go smoothly"),
                         "answer": interperate_rating(report.cooperation)},
                        {"question": ("[Initiative] Seeing what needs to be done and doing it without"
                                      " someone asking them to"),
                         "answer": interperate_rating(report.initiative)},
                        {"question": ("[Team Focus] Interested in the entire project and its progress, not"
                                      " just exclusively thinking about their part"),
                         "answer": interperate_rating(report.team_focus)},
                        {"question": ("[Contribution] Assess this person's overall contribution to the"
                                      " project"),
                         "answer": interperate_rating(report.contribution)},
                        {"question": "[Leadership]",
                         "answer": interperate_rating(report.leadership)},
                        {"question": "[Organization]",
                         "answer": interperate_rating(report.organization)},
                        {"question": "[Delegation]",
                         "answer": interperate_rating(report.delegation)},
                        {"question": ("Points for this teammate. (A number between 0 and 100. Give yourself"
                                      " 0. Points across all reviews should add to 100)"),
                         "answer": report.points},
                        {"question": "Please comment on this person's strengths",
                         "answer": report.strengths},
                        {"question": "Please comment on this person's weaknesses",
                         "answer": report.weaknesses},
                        {"question": ("Suggest one trait you think this person should work on to become a"
                                      " better team member"),
                         "answer": report.traits_to_work_on}
                ]

                # Final Reviews will have some extra details
                if report.is_final:
                    parsed_review.append({"question": "What did you learn from this experience",
                                          "answer": reports.what_you_learned})
                    if reviewer_id == reviewee_id:
                        parsed_review.append({"question": ("Are you proud of your team's product and your:"
                                                           " role in it? Please explain"),
                                              "answer": reports.proud_of_accomplishment})

                # Send the data off to the client
                return render_template("viewReview.html", details=review_details, review_data=parsed_review)
            else:
                error = "We couldn't find the report :("
                return render_template('viewReview.html', error=error)

        # https://stackoverflow.com/questions/47719838/how-to-catch-all-exceptions-in-try-catch-block-python
        except Exception:
            error = "Something went wrong :("
            return render_template('viewReview.html', error=error)
