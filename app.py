from flask import Flask, redirect, request, url_for, render_template
from flask.views import MethodView
import dashboard
from index import Index
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from form import form_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capstone360.db'
app.config['SECRET_KEY'] = 'NotSoSecret'
engine = create_engine('sqlite:///capstone360.db', convert_unicode=True, echo=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

#form blueprint, can change to url_rules without blueprint if desired
app.register_blueprint(form_bp)

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
This is for the dashboard page view
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
