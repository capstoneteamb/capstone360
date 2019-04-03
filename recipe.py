from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Recipe(MethodView):
    def get(self):
        """
        get data from model
        """
        model = gbmodel.get_model()
        #cookbook = model.select()
        cookbook = [dict(title=row[0], author=row[1], ingredients=row[2], time=row[3], skill=row[4], description=row[5], image=row[6], date_submitted=row[7]) for row in model.select()]
        return render_template('recipe.html',cookbook=cookbook)