from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Dashboard(MethodView):
    def get(self):
        """
        get data from model
        """
        model = gbmodel.get_model()
        students = [dict(name=row[3]) for row in model.selectStudents()]
        return render_template('dashboard.html', students=students)
