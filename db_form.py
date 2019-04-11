import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

team_members = db.Table('team_members',
    db.Column('tid', db.Integer, db.ForeignKey('teams.id'), unique=False, nullable=False, primary_key=True),
    db.Column('sid', db.Integer, db.ForeignKey('students.id'), unique=False, nullable=False, primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('capstone_session.id'), unique=False, nullable=False, primary_key=True)
)

class students(db.Model):
    id = db.Column(db.String(128), unique=False, nullable=False, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=False, nullable=False, primary_key=False)
    session_id = db.Column(db.Integer, db.ForeignKey('capstone_session.id'), unique=False, nullable=False, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False, primary_key=False)
    is_lead = db.Column(db.Boolean, unique=False, nullable=False, primary_key=False)
    midterm_done = db.Column(db.Boolean, unique=False, nullable=False, default=False, primary_key=False)
    final_done = db.Column(db.Boolean, unique=False, nullable=False, default=False, primary_key=False)
    active = db.Column(db.String(128), nullable=True, default=None)

    #sess = db.relationship('capstone_session', foreign_keys='capstone_session.id')
    #team_id = db.relationship('teams', foreign_keys='teams.id')


class teams(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('capstone_session.id'), nullable=False, primary_key=False)
    #capstone_session = db.relationship('capstone_session', backref=db.backref('cid', lazy=False))
    name = db.Column(db.String(128), nullable=False, unique=False, primary_key=False)

class capstone_session(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    start_term = db.Column(db.String(10), nullable=False, unique=False, primary_key=False)
    start_year = db.Column(db.Integer, nullable=False, unique=False, primary_key=False)
    end_term = db.Column(db.String(10), nullable=False, unique=False, primary_key=False)
    end_year = db.Column(db.Integer, nullable=False, unique=False, primary_key=False)

class reports(db.Model):
    time = db.Column(db.DateTime, unique=False, nullable=False, primary_key=False)
    session_id = db.Column(db.Integer, db.ForeignKey('capstone_session.id'), unique=False, nullable=False, primary_key=False)
    reporting = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False, nullable=False, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=False, nullable=False, primary_key=True)
    report_for = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False, nullable=False, primary_key=True)
    tech_mastery = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    work_ethic = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    communication = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    cooperation = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    initiative = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    team_focus = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    contribution = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    leadership = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    organization = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    delegation = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    points = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    strengths = db.Column(db.String(4096), unique=False, nullable=True, primary_key=False)
    weaknesses = db.Column(db.String(4096), unique=False, nullable=True, primary_key=False)
    traits_to_work_on = db.Column(db.String(4096), unique=False, nullable=True, primary_key=False)
    what_you_learned = db.Column(db.String(4096), unique=False, nullable=True, primary_key=False)
    proud_of_accomplishment = db.Column(db.String(4096), unique=False, nullable=True, primary_key=False)
    is_final = db.Column(db.Boolean, unique=False, nullable=False, primary_key=True)

