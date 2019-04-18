from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from db_form import db, capstone_session, teams, students, team_members, reports
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import datetime
import gbmodel

def get_teams():
    return db.session.query(teams)

def get_members():
    return db.session.query(students.name, students.tid).filter(students.tid == teams.id)

def choice_query():
    return db.session.query(capstone_session)

class Form(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='start_year', blank_text='Select Term')
