"""
This is the sqlite database for the recipe flask app
+---------+----------+---------------+------+--------+-------------------+---------------+------------------+
| Title   | Author   | Ingredients   | Time |  Skill | Description       | Image         |  Date Submitted  |
+=========+==========+===============+======+========+===================+===============+==================+
| Pizza   | Mike     | dough, cheese |  45  |   4    | Prepare dough...  | https://...   |   2017-10-25     |
+---------+----------+---------------+------+--------+-------------------+---------------+------------------+
"""

from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'recipes.db'

class model(Model):
    def __init__(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from recipes")
        except sqlite3.OperationalError:
            cursor.execute("create table recipes (title, author, ingredients, time, skill, description, image, date_submitted)")
        cursor.close()
    
    def select(self):
        """
        Get all rows from the recipe database
        Each row contains: title, author, ingredients, time, skill, description, image, date_submitted
        :return List of lists containg all row of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recipes")
        return cursor.fetchall()
    
    def insert(self, title, author, ingredients, time, skill, description, image):
        """
        Insert data into the database
        :param title: String
        :param author: String
        :param ingredients: String
        :param time: String
        :param skill: String
        :param description: String
        :param image: String
        """
        

        params = {'title': title, 'author': author, 'ingredients': ingredients, 'time': time, 'skill': skill, 'description': description, 'image': image, 'date_submitted': date.today()}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into recipes (title, author, ingredients, time, skill, description, image, date_submitted) VALUES (:title, :author, :ingredients, :time, :skill, :description, :image, :date_submitted)", params)

        connection.commit()
        cursor.close()
        return True