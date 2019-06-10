from flask import request, make_response, render_template
from flask.views import MethodView
from flask_cas import login_required
from common_functions import display_access_control_error

import gbmodel


class MissingStudentException(Exception):
    """
    We raise this exception if we find no students for a given team or session, to be more explicit than eg.
    a KeyError.
    """
    pass


class MissingTeamException(Exception):
    """
    We raise this exception if we don't find a team in the database when we look it up by id
    """
    pass


class GeneratedProfessorReportView(MethodView):
    @login_required
    def get(self):
        """
        Generates a report for a specific student, for viewing by a professor.
        Specifically, generates a single report, for a single session and term (midterm or final), for a
        single student, with comments deanonymized.
        """
        if not validate_professor():
            return display_access_control_error()

        student_id = request.args.get('student_id')
        session_id = request.args.get('session_id')
        is_final = request.args.get('is_final')
        # TODO find a less fragile way to deal with booleans in urls
        if is_final == "False":
            is_final = False
        else:
            is_final = True

        try:
            pdf = _make_student_report_pdf(student_id, session_id, is_final, is_professor_report=True)
            response = make_response(pdf)
        except MissingStudentException:
            response = make_response(render_template('404.html'), 404)

        return response


class GeneratedAnonymousReportView(MethodView):
    @login_required
    def get(self):
        """
        Generates all anonymized reports for printing and handing out to students.
        """
        if not validate_professor():
            return display_access_control_error()

        session_id = request.args.get('session_id')
        is_final = request.args.get('is_final')
        # TODO find a less fragile way to deal with booleans in urls
        if is_final == "False":
            is_final = False
        else:
            is_final = True

        try:
            pdf = _make_printable_reports(session_id, is_final)
            response = make_response(pdf)
        except MissingStudentException:
            response = make_response(render_template('404.html'), 404)

        return response


def _make_printable_reports(session_id, is_final):
    """
    Compiles all reports for a session into one for printing.
    This means we generate a bunch of anonymized reports, then concatenate them, since page breaks are
    handled in the HTML template.

    Keyword arguments:
    session_id -- session to generate reports for
    is_final -- if True, makes a final report. If False, generates a midterm report.
    """
    students = gbmodel.students().get_students_in_session(session_id)
    if students is None or len(students) <= 0:
        raise MissingStudentException("No students for this session.")

    report = ""

    # Concatenate anonymized reports for all students on the team
    for s in students:
        report = report + _make_student_report_pdf(s.id, session_id, is_final)
    return report


def _make_student_report_pdf(student_id, session_id, is_final, is_professor_report=False):
    """
    Renders a report for a student, defaulting to the results of their midterm review.
    Unless is_professor_report is set to True, the report will be anonymized.

    Keyword arguments:
    student_id -- id of the student to generate a report for
    session_id -- session to generate reports for
    is_final -- if True, makes a final report. If False, generates a midterm report.
    is_professor_report -- if True, makes a deanonymized report. If False, generates an anonymous report.
    """
    # Get all the info we need to compile the report
    reports = gbmodel.reports().get_reports_for_student(student_id, session_id, is_final)
    student = gbmodel.students().get_student_in_session(student_id, session_id)

    if student is None:
        raise MissingStudentException("Trying to generate a report for a student that doesn't exist.")

    name = student.name
    team_id = student.tid
    team = gbmodel.teams().get_team_from_id(team_id)

    if team is None:
        raise MissingTeamException("The student's team does not appear to exist.")

    team_name = team.name

    # init scores so we can tally how many 1s we got, 2s, etc.
    scores = {
            'tech_mastery': [],
            'work_ethic': [],
            'communication': [],
            'cooperation': [],
            'initiative': [],
            'team_focus': [],
            'contribution': [],
            'leadership': [],
            'organization': [],
            'delegation': []
            }

    for _, value in scores.items():
        for i in range(6):
            value.append(0)

    # Do any calculations we need to fill in the table.
    # Compile all strengths and weaknesses into a list, tally up scores, etc.
    strengths = []
    weaknesses = []
    traits_to_work_on = []

    # These two fields are only on self reviews.
    what_you_learned = None
    proud_of_accomplishment = None

    # Iterate through all reports, tallying scores.
    # As we go we also collect a list of all the text box answers.
    points = 0
    for r in reports:
        for key, value in scores.items():
            this_score = getattr(r, key)
            # 6 = N/A in the table
            if this_score is None:
                this_score = 6
            # Increment the # of votes for this score. Ratings start at 1 and not 0 so we have to shift
            # things left by one in the table.
            scores[key][this_score-1] = scores[key][this_score-1] + 1

        # If this is for the professor, all the comments should have names attached.
        if is_professor_report:
            reporter = gbmodel.students().get_student_in_session(r.reviewer, session_id)

            if reporter is None:
                raise MissingStudentException("The reporting student in a review doesn't exist.")

            weaknesses.append("{}: {}".format(reporter.name, r.weaknesses))
            strengths.append("{}: {}".format(reporter.name, r.strengths))
            traits_to_work_on.append("{}: {}".format(reporter.name, r.traits_to_work_on))

            # There are a handful of fields we only display if it's a professor and a self review.
            if r.reviewer == student_id:
                # what you learned always
                what_you_learned = r.what_you_learned
                # proud_of_accomplishment only applies for finals
                proud_of_accomplishment = r.proud_of_accomplishment

        # If this is the student's self review, the comments get marked with asterisks.
        elif r.reviewer == student_id:
            weaknesses.append("**{}".format(r.weaknesses))
            strengths.append("**{}".format(r.strengths))
            traits_to_work_on.append("**{}".format(r.traits_to_work_on))

        else:
            weaknesses.append(r.weaknesses)
            strengths.append(r.strengths)
            traits_to_work_on.append(r.traits_to_work_on)

        # Tally up points
        points += r.points

    # Mark all the self reported scores
    for r in reports:
        if r.reviewer == student_id:
            for key, value in scores.items():
                this_score = getattr(r, key)
                if this_score is not None:
                    scores[key][this_score-1] = "**{}".format(scores[key][this_score-1])

    # Render the HTML version of the template
    html = render_template('report.html',
                           name=name,
                           team=team_name,
                           scores=scores,
                           points=points,
                           strengths=strengths,
                           weaknesses=weaknesses,
                           traits_to_work_on=traits_to_work_on,
                           what_you_learned=what_you_learned,
                           proud_of_accomplishment=proud_of_accomplishment)

    return html
