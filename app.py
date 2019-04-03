#!/usr/bin/env python3
"""
A simple recipe flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from recipe import Recipe
from add import Add

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

"""
This is for the recipe page view
"""
app.add_url_rule('/recipe/',
                view_func=Recipe.as_view('recipe'),
                methods=['GET'])


"""
This is for the recipe add page view
"""
app.add_url_rule('/add/',
                view_func=Add.as_view('add'),
                methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
