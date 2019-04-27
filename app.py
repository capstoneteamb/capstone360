from flask import Flask, redirect, request, url_for, render_template
from flask.views import MethodView
from index import Index
import dashboard
from add_remove import Dashboard
from add_remove import AddTeam
from add_remove import AddStudent
from add_remove import RemoveTeam
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:///capstone360.db', convert_unicode=True, echo=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

app.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard'),
                methods=['GET', 'POST'])

app.add_url_rule('/addStudent/',
                view_func=AddStudent.as_view('addStudent'),
                methods=['GET', 'POST'])
                
app.add_url_rule('/addTeam/',
                view_func=AddTeam.as_view('addTeam'),
                methods=['GET', 'POST'])

app.add_url_rule('/removeTeam/',
                view_func=RemoveTeam.as_view('removeTeam'),
                methods=['GET', 'POST'])

if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=8000, debug=True)
