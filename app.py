"""
Flask entry
"""
from flask import Flask, render_template
import dashboard
import removeDashboard
from add import AddTeam
from add import AddStudent
from index import Index
from remove import RemoveStudent
from remove import RemoveTeam
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from form import form_bp
from flask_cas import CAS
from flask_cas import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:///capstone360.db', convert_unicode=True, echo=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

#CAS LOGIN
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

@app.route('/dashboard/', methods=['GET','POST'])
@login_required
def get():
    lists = dashboard.get()
    print(lists)
    if lists is False:
        return render_template('index.html')
    sessions = {'first','second'}
    return render_template('dashboard.html', lists = lists, sessions=sessions)

@app.route('/logout/')
def logged_out():
    # return redirect (url_for('index'))
    return render_template('index.html')

@app.route('/removeDashboard/', methods=['GET','POST'])
@login_required
def get_rm():
    lists = removeDashboard.get_rm()
    return render_template('removeDashboard.html', lists=lists)


app.add_url_rule('/addStudent/',
                 view_func=AddStudent.as_view('addStudent'),
                 methods=['GET', 'POST'])

app.add_url_rule('/addTeam/',
                 view_func=AddTeam.as_view('addTeam'),
                 methods=['GET', 'POST'])

app.add_url_rule('/removeStudent/',
                 view_func=RemoveStudent.as_view('removeStudent'),
                 methods=['GET', 'POST'])

app.add_url_rule('/removeTeam/',
                 view_func=RemoveTeam.as_view('removeTeam'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
