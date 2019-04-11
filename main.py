from flask import Flask, render_template, request, jsonify, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\faisa\\Desktop\\Code\\capstone\\mockup_database.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:///C:\\Users\\faisa\\Desktop\\Code\\capstone\\mockup_database.db', convert_unicode=True, echo=False)

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

class teams(db.Model):
    __table__ = db.Model.metadata.tables['teams']

    def __repr__(self):
        return self.DISTRICT

class team_members(db.Model):
    __table__ = db.Model.metadata.tables['team_members']

    def __repr__(self):
        return self.DISTRICT

class students(db.Model):
    __table__ = db.Model.metadata.tables['students']

    def __repr__(self):
        return self.DISTRICT
        
class reports(db.Model):
    __table__ = db.Model.metadata.tables['reports']

    def __repr__(self):
        return self.DISTRICT

class capstone_session(db.Model):
    __table__ = db.Model.metadata.tables['capstone_session']

    #def __repr__(self):
        #return self.start_term

class removed_students(db.Model):
    __table__ = db.Model.metadata.tables['removed_students']

    def __repr__(self):
        return self.DISTRICT

def choice_query():
    return db.session.query(capstone_session)

class Form(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='start_year')



@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = Form()
    team_names = db_session.query(teams)
    member_names = db_session.query(students)
    #member_names = db_session.query(students.name).filter(teams.id==students.tid)
    
    return render_template('home.html', team_names=team_names, member_names=member_names, form=form)

if __name__ == "__main__":
    app.run(debug=True)

   # for d in db_session.query(team_members):
   #     if d.tid == 1:
   #         print("yes")
    #for item in db_session.query(capstone_session):
    #    print(item)
