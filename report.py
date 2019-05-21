from flask import request, make_response, render_template
from flask.views import MethodView
from flask_cas import login_required

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

        if is_professor_report:
            reporter = gbmodel.students().get_student_in_session(r.reviewer, session_id)

            if reporter is None:
                raise MissingStudentException("The reporting student in a review doesn't exist.")

            weaknesses.append(reporter.name + ": " + r.weaknesses)
            strengths.append(reporter.name + ": " + r.strengths)
        else:
            weaknesses.append(r.weaknesses)
            strengths.append(r.strengths)

        # Tally up points
        points += r.points

    # Mark all the self reported scores
    for r in reports:
        if r.reviewer == student_id:
            for key, value in scores.items():
                this_score = getattr(r, key)
                scores[key][this_score-1] = "**{}".format(scores[key][this_score-1])

    # Render the HTML version of the template
    html = render_template('report.html',
                           name=name,
                           team=team_name,
                           scores=scores,
                           points=points,
                           strengths=strengths,
                           weaknesses=weaknesses)

    return html
