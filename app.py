"""
A simple recipe flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from dashboard import Dashboard
from add import AddStudent
from add import AddTeam
from remove import RemoveStudent
from remove import RemoveTeam
from removeDashboard import RemoveDashboard


app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
This is for the dashboard page view
"""
app.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard'),
                methods=['GET'])

"""
This is for the remove dashboard page view
"""
app.add_url_rule('/removeDashboard/',
                view_func=RemoveDashboard.as_view('removeDashboard'),
                methods=['GET'])
                
"""
This is for the add student page view
"""
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
    app.run(host='0.0.0.0', port='8000', debug=True)
