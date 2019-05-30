"""
Flask entry
"""
from flask import Flask

from extensions import db, cas

import os


def create_app(debug=False):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'
    app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CAS_SERVER'] = 'https://auth.cecs.pdx.edu/cas/login'
    app.config['CAS_AFTER_LOGIN'] = 'dashboard'
    app.config['CAS_AFTER_LOGOUT'] = 'logout'
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    if not debug:
        os.environ['CAPSTONE_SETTINGS'] = '/etc/capstone.prod.cfg'
        app.config.from_envvar('CAPSTONE_SETTINGS')

    app.app_context().push()
    db.init_app(app)
    db.Model.metadata.reflect(db.engine)

    # CAS LOGIN
    cas.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    from index import Index
    from form import review
    from prof_dashboard import ProfDashboard
    from prof_dashboard import AddTeam
    from prof_dashboard import AddStudent
    from prof_dashboard import AddTeamCSV
    from prof_dashboard import RemoveTeam
    from prof_dashboard import SetDate
    from prof_dashboard import AddSession
    from prof_dashboard import AssignTeam
    from prof_dashboard import RemoveSession
    from student_dashboard import StudentDashboard
    from student_dashboard import EditStudent
    from student_register import StudentRegister
    from report import GeneratedProfessorReportView, GeneratedAnonymousReportView
    from view_student import ViewStudent
    from view_review import ViewReview

    app.add_url_rule('/',
                     view_func=Index.as_view('index'))

    app.add_url_rule('/studentDashboard/',
                     view_func=StudentDashboard.as_view('studentDashboard'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/editStudent',
                     view_func=EditStudent.as_view('editStudent'),
                     methods=['GET'])

    app.add_url_rule('/review/<capstone_id>',
                     view_func=review.as_view('review'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/profDashboard/',
                     view_func=ProfDashboard.as_view('profDashboard'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/addStudent/',
                     view_func=AddStudent.as_view('addStudent'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/addTeamCSV/',
                     view_func=AddTeamCSV.as_view('addTeamCSV'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/assignTeam/',
                     view_func=AssignTeam.as_view('assignTeam'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/addSession/',
                     view_func=AddSession.as_view('addSession'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/removeSession/',
                     view_func=RemoveSession.as_view('removeSession'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/addTeam/',
                     view_func=AddTeam.as_view('addTeam'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/removeTeam/',
                     view_func=RemoveTeam.as_view('removeTeam'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/setDate/',
                     view_func=SetDate.as_view('setDate'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/professorReport/',
                     view_func=GeneratedProfessorReportView.as_view('professorReport'),
                     methods=['GET'])

    app.add_url_rule('/studentReport/',
                     view_func=GeneratedAnonymousReportView.as_view('studentReport'),
                     methods=['GET'])

    app.add_url_rule('/register/',
                     view_func=StudentRegister.as_view('registerStudent'),
                     methods=['GET', 'POST'])

    app.add_url_rule('/viewStudent/',
                     view_func=ViewStudent.as_view('viewStudent'),
                     methods=['POST'])

    app.add_url_rule('/viewReview/',
                     view_func=ViewReview.as_view('viewReview'),
                     methods=['POST'])


if __name__ == '__main__':
    app = create_app(debug=True)
    app.run(host='0.0.0.0', port=8000)
