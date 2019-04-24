from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import datetime
import dashboard
from app import cas
from flask_cas import login_required

def validate():
    username = cas.username
    students = gbmodel.students()
    found = students.validate(username)
    print(found," in validate")
    if found is None:
        return False
    return True
