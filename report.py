from flask import request, make_response, render_template
from flask.views import MethodView

import gbmodel

class TeamReportListView(MethodView):
    def get(self, team_id):
        """
        Renders a list of reports for a specific team.
        """
        # Make list of students on this team
        students = gbmodel.students.query.filter_by(tid=team_id, session_id=0)
        return render_template('reportList.html', students=students)

class GeneratedReportView(MethodView):

    def get(self):
        """
        Generates a report for a specific student.
        """
        student_id = request.args.get('student_id')
        session_id = request.args.get('session_id')
        is_final = request.args.get('is_final')
        # TODO find a less fragile way to deal with booleans in urls
        if is_final == "False":
            is_final = False
        else:
            is_final = True

        pdf = _make_student_report_pdf(student_id, session_id, is_final)
        response = make_response(pdf)
        return response

def _make_student_report_pdf(student_id, session_id, is_final):
    """
    Renders a pdf for a student, defaulting to midterm review.
    """
    # Get all the info we need to compile the report
    print("student: {} session: {} is_final: {}".format(student_id, session_id, is_final))
    reports = gbmodel.reports().get_reports_for_student(student_id, session_id, is_final)
    student = gbmodel.students.query.filter_by(id=student_id, session_id=session_id).first()
    name = student.name
    team_id = student.tid
    team_name = gbmodel.teams.query.filter_by(id=team_id, session_id=session_id).first().name

    # init scores
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

    for _,value in scores.items():
        for i in range(6):
            value.append(0)

    # Do any calculations we need to fill in the table.
    # Compile all strengths and weaknesses into a list, tally up scores, etc.
    strengths = []
    weaknesses = []
    for r in reports:
        for key,value in scores.items():
            this_score = getattr(r,key)
            if this_score is None:
                this_score = 6
            # Increment the # of votes for this score. Ratings start at 1 and not 0 so we have to shift
            # things left by one in the table.
            scores[key][this_score-1] = scores[key][this_score-1] + 1

        weaknesses.append(r.weaknesses)
        strengths.append(r.strengths)

    # TODO Mark all the self reported scores
    for r in reports:
        if r.reporting == student_id:
            pass

    # Render the HTML version of the template
    html = render_template('report.html',
            name=name,
            team=team_name,
            scores=scores,
            strengths=strengths,
            weaknesses=weaknesses)

    return html
