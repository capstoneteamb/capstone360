from flask import request, make_response
from flask.views import MethodView

from fpdf import FPDF

import gbmodel

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
        pdf = _make_student_report('asdf')
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename={}.pdf'.format('asdf')
        return response

def _make_student_report(username):
    """
    Renders a pdf for a username.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    return pdf.output(dest="S").encode('latin-1')
