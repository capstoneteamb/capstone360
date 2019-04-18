"""
Entry into the Flask App
"""
import flask
from flask import Flask, redirect, request, url_for, render_template
from flask.views import MethodView
import dashboard 
from index import Index
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from db_form import db, capstone_session, teams, students, team_members, reports
from db_form import db
from form import form_bp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\faisa\\Desktop\\Code\\capstone\\capstone360.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:///C:\\Users\\faisa\\Desktop\\Code\\capstone\\capstone360.db', convert_unicode=True, echo=False)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
app.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard'),
                methods=['GET', 'POST'])
"""

@app.route('/dashboard/')
@app.route('/dashboard/', methods=['GET','POST'])
def get():
    lists = dashboard.get()
    form = dashboard.Form()
    team_names = dashboard.get_teams()
    member_names = dashboard.get_members()
    """
    dic_of_names = {}
    m = dashboard.get_tid()
    for i in m:
        dic_of_names[i] = dashboard.get_members(i)
    """
    #print(dic_of_names)
    return render_template('dashboard.html', lists = lists, team_names=team_names, member_names=member_names, form=form) 

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8000, debug=True)

    app.run(debug=True)
