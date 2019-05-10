"""
Flask entry
"""
from flask import Flask
from index import Index

import dashboard  # noqa
from prof_dashboard import Dashboard
from prof_dashboard import AddTeam
from prof_dashboard import AddStudent
from csvAddTeam     import AddTeamCSV
from prof_dashboard import RemoveTeam
from prof_dashboard import SetDate
from report import TeamReportListView, GeneratedProfessorReportView, GeneratedAnonymousReportView
from view_student import ViewStudent
from view_review import ViewReview
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from form import review
from flask_cas import CAS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:///capstone360.db', convert_unicode=True, echo=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

# CAS LOGIN
cas = CAS()
cas.init_app(app)
app.config['CAS_SERVER'] = 'https://auth.cecs.pdx.edu/cas/login'
app.config['CAS_AFTER_LOGIN'] = 'dashboard'
app.config['CAS_AFTER_LOGOUT'] = 'logout'

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

app.add_url_rule('/review/',
                 view_func=review.as_view('review'),
                 methods=['GET', 'POST'])

app.add_url_rule('/dashboard/',
                 view_func=Dashboard.as_view('dashboard'),
                 methods=['GET', 'POST'])

app.add_url_rule('/addStudent/',
                 view_func=AddStudent.as_view('addStudent'),
                 methods=['GET', 'POST'])

app.add_url_rule('/addTeam/',
                 view_func=AddTeam.as_view('addTeam'),
                 methods=['GET', 'POST'])

app.add_url_rule('/addTeamCSV/',
                 view_func=AddTeamCSV.as_view('addTeamCSV'),
                 methods=['GET', 'POST'])

app.add_url_rule('/removeTeam/',
                 view_func=RemoveTeam.as_view('removeTeam'),
                 methods=['GET', 'POST'])

app.add_url_rule('/setDate/',
                 view_func=SetDate.as_view('setDate'),
                 methods=['GET', 'POST'])

app.add_url_rule('/reportList/<team_id>',
                 view_func=TeamReportListView.as_view('reportList'),
                 methods=['GET'])

app.add_url_rule('/professorReport/',
                 view_func=GeneratedProfessorReportView.as_view('professorReport'),
                 methods=['GET'])

app.add_url_rule('/studentReport/',
                 view_func=GeneratedAnonymousReportView.as_view('studentReport'),
                 methods=['GET'])

app.add_url_rule('/viewStudent/',
                 view_func=ViewStudent.as_view('viewStudent'),
                 methods=['POST'])

app.add_url_rule('/viewReview/',
                 view_func=ViewReview.as_view('viewReview'),
                 methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
