"""
Entry into the Flask App
"""
import flask
from flask.views import MethodView
from index import Index
from dashboard import Dashboard

app = flask.Flask(__name__)

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
This is for the dashboard page view
"""
app.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard'),
                methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
