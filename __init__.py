# main file for server management
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_form import db, capstone_session, teams, students, team_members, reports

#db = SQLAlchemy


def fill_data(db):
    term1 = capstone_session()
    term1.id = 3
    term1.start_term = 'wtr'
    term1.end_term = 'spr'
    term1.start_year = '19'
    term1.end_year = '19'
    db.session.add(term1)

    team1 = teams()
    team1.id = 11
    team1.session_id = 1
    team1.name = 'trek'
    db.session.add(team1)

    picard = students()
    picard.id = 45
    picard.tid = 11
    picard.session_id = 3
    picard.name = 'picard'
    picard.midterm_done = 0
    picard.final_done = 0
    picard.active = 'midterm'
    picard.is_lead = 1
    db.session.add(picard)

    sisko = students()
    sisko.id = 46
    sisko.tid = 11
    sisko.session_id = 3
    sisko.name = 'sisko'
    sisko.midterm_done = 0
    sisko.final_done = 0
    sisko.active = 'midterm'
    sisko.is_lead = 0
    db.session.add(sisko)

    janeway = students()
    janeway.id = 47
    janeway.tid = 11
    janeway.session_id = 3
    janeway.name = 'janeway'
    janeway.midterm_done = 0
    janeway.final_done = 0
    janeway.active = 'midterm'
    janeway.is_lead = 0
    db.session.add(janeway)

    kirk = students()
    kirk.id = 48
    kirk.tid = 11
    kirk.session_id = 3
    kirk.name = 'kirk'
    kirk.midterm_done = 0
    kirk.final_done = 0
    kirk.active = 'midterm'
    kirk.is_lead = 0
    db.session.add(kirk)
    


    add_rel1 = team_members.insert().values(tid=11, sid=45, session_id=3)
    add_rel2 = team_members.insert().values(tid=11, sid=46, session_id=3)
    add_rel3 = team_members.insert().values(tid=11, sid=47, session_id=3)
    add_rel4 = team_members.insert().values(tid=11, sid=48, session_id=3)
    db.session.execute(add_rel1)
    db.session.execute(add_rel2)
    db.session.execute(add_rel3)
    db.session.execute(add_rel4)

    db.session.commit()
    print('db set')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='NotSoSecret',
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.db'

    #from . import db
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        fill_data(db)

    from . import form
    app.register_blueprint(form.bp)

    return app
