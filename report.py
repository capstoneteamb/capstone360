from flask import request, make_response, render_template
from flask.views import MethodView

from fpdf import FPDF, HTMLMixin

import gbmodel

class MyFPDF(FPDF, HTMLMixin):
    pass

class StudentReportListView(MethodView):
    def get(self):
        """
        Renders a list of reports for a specific student.
        """
        pass


class TeamReportListView(MethodView):
    def get(self):
        """
        Renders a list of reports for a specific team.
        """
        pass

class GeneratedReportView(MethodView):

    def get(self):
        """
        Accepts a GET request and generates a report for a specific student.
        Should be POST once this PDF is filled with actual data
        """
        pdf = _make_student_report_pdf(0, 0, False)
        response = make_response(pdf)
        #response.headers['Content-Type'] = 'application/pdf'
        #response.headers['Content-Disposition'] = \
        #    'inline; filename={}.pdf'.format('asdf')
        return response

def _make_student_report_pdf(student_id, term_id, is_final):
    """
    Renders a pdf for a student, defaulting to midterm review.
    """
    # Get all the info we need to compile the report
    reports = gbmodel.reports.get_reports_for_student(student_id, term_id, is_final)
    name = gbmodel.students.query.filter_by(id=student_id).first().name
    team = "Sample Team"

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
            # Increment the # of votes for this score. Ratings start at 1 and not 0 so we have to shift
            # things left by one in the table.
            scores[key][this_score-1] = scores[key][this_score] + 1

        weaknesses.append(r.weaknesses)
        strengths.append(r.strengths)

    # TODO Mark all the self reported scores
    for r in reports:
        if r.reporting == student_id:
            pass

    # Render the HTML version of the template
    html = render_template('report.html',
            name=name,
            team=team,
            scores=scores,
            strengths=strengths,
            weaknesses=weaknesses)

    return html
