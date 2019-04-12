"""
Entry into the Flask App
"""
import flask
from flask.views import MethodView
from index import Index
from dashboard import Dashboard
from flask_sqlalchemy import SQLAlchemy
from db_form import db, capstone_session, teams, students, team_members, reports
from form import form_bp

app = flask.Flask(__name__)

app.config.from_mapping(
        SECRET_KEY='NotSoSecret',
    )

#will change to capstone360.db when updated
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.db'
db.init_app(app)


#will remove when capstone360.db is updated
updt = 1
with app.app_context():
    if updt == 1:
        db.drop_all()
        db.create_all()
        term1 = capstone_session()
        term1.id = 3
        term1.start_term = 'wtr'
        term1.end_term = 'spr'
        term1.start_year = '19'
        term1.end_year = '19'
        db.session.add(term1)

        term2 = capstone_session()
        term2.id = 5
        term2.start_term = 'spr'
        term2.end_term = 'smr'
        term2.start_year = '19'
        term2.end_year = '19'
        db.session.add(term2)

        team1 = teams()
        team1.id = 11
        team1.session_id = 3
        team1.name = 'trek'
        db.session.add(team1)

        team2 = teams()
        team2.id = 22
        team2.session_id = 3
        team2.name = 'lotr'
        db.session.add(team2)

        team3 = teams()
        team3.id = 33
        team3.session_id = 5
        team3.name = 'gw'
        db.session.add(team3)

        picardy = students()
        picardy.id = 45
        picardy.tid = 11
        picardy.session_id = 3
        picardy.name = 'picardy'
        picardy.midterm_done = 0
        picardy.final_done = 0
        picardy.active = 'midterm'
        picardy.is_lead = 1
        db.session.add(picardy)

        ben = students()
        ben.id = 46
        ben.tid = 11
        ben.session_id = 3
        ben.name = 'ben'
        ben.midterm_done = 0
        ben.final_done = 0
        ben.active = 'midterm'
        ben.is_lead = 0
        db.session.add(ben)

        cat = students()
        cat.id = 47
        cat.tid = 11
        cat.session_id = 3
        cat.name = 'cat'
        cat.midterm_done = 0
        cat.final_done = 0
        cat.active = 'midterm'
        cat.is_lead = 0
        db.session.add(cat)

        tiber = students()
        tiber.id = 48
        tiber.tid = 11
        tiber.session_id = 3
        tiber.name = 'tiber'
        tiber.midterm_done = 0
        tiber.final_done = 0
        tiber.active = 'midterm'
        tiber.is_lead = 0
        db.session.add(tiber)

        sam = students()
        sam.id = 55
        sam.tid = 22
        sam.session_id = 3
        sam.name = 'sam'
        sam.midterm_done = 0
        sam.final_done = 0
        sam.active = 'final'
        sam.is_lead = 1
        db.session.add(sam)

        john = students()
        john.id = 56
        john.tid = 22
        john.session_id = 3
        john.name = 'john'
        john.midterm_done = 0
        john.final_done = 0
        john.active = 'final'
        john.is_lead = 0
        db.session.add(john)

        ronald = students()
        ronald.id = 57
        ronald.tid = 22
        ronald.session_id = 3
        ronald.name = 'ronald'
        ronald.midterm_done = 0
        ronald.final_done = 0
        ronald.active = 'final'
        ronald.is_lead = 0
        db.session.add(ronald)

        caran = students()
        caran.id = 58
        caran.tid = 22
        caran.session_id = 3
        caran.name = 'caran'
        caran.midterm_done = 0
        caran.final_done = 0
        caran.active = 'final'
        caran.is_lead = 0
        db.session.add(caran)

        com = students()
        com.id = 65
        com.tid = 33
        com.session_id = 5
        com.name = 'com'
        com.midterm_done = 1
        com.final_done = 1
        com.active = 'midterm'
        com.is_lead = 0
        db.session.add(com)

        add_rel1 = team_members.insert().values(tid=11, sid=45, session_id=3)
        add_rel2 = team_members.insert().values(tid=11, sid=46, session_id=3)
        add_rel3 = team_members.insert().values(tid=11, sid=47, session_id=3)
        add_rel4 = team_members.insert().values(tid=11, sid=48, session_id=3)
        db.session.execute(add_rel1)
        db.session.execute(add_rel2)
        db.session.execute(add_rel3)
        db.session.execute(add_rel4)

        add_rel5 = team_members.insert().values(tid=22, sid=55, session_id=3)
        add_rel6 = team_members.insert().values(tid=22, sid=56, session_id=3)
        add_rel7 = team_members.insert().values(tid=22, sid=57, session_id=3)
        add_rel8 = team_members.insert().values(tid=22, sid=58, session_id=3)
        db.session.execute(add_rel5)
        db.session.execute(add_rel6)
        db.session.execute(add_rel7)
        db.session.execute(add_rel8)

        add_rel9 = team_members.insert().values(tid=33, sid=65, session_id=5)
        db.session.execute(add_rel9)
        db.session.commit()

#form blueprint, can change to url_rules without blueprint if desired
app.register_blueprint(form_bp)

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
This is for the dashboard page view
"""
app.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard'),
                methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
