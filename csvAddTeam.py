import os
import sqlite3
import io
import csv
from flask import Flask, render_template, request, g
app = Flask(__name__)

@app.route("/csvAddTeam", methods=['GET', 'POST'])
def csvAddTeam():
	#Database variables
	db = sqlite3.connect('mockup_database.db') # Connect to the database
	accessor = db.cursor() # This is used to access and make changes to the db
	if request.method=='POST':
		file = request.files['teamcsv']
		stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
		csv_reader = csv.reader(stream, delimiter=',')
		for row in csv_reader:
			teamName = row[0]
			students = []
			i = 1 # Incrementor for while loop
			while i < len(row):
				students.extend([row[i]])
				i+=1
			accessor.execute('SELECT MAX(id) FROM teams') #Find the highest id value in the team table
			nextID = 1+accessor.fetchone()[0] # Get the next unique ID value
			accessor.execute('INSERT INTO teams VALUES(?,?,?)',
											(nextID,0,teamName))
			for s in students:
				accessor.execute('UPDATE students SET tid = ? WHERE name=?',(nextID,s))

			db.commit()
			db.close()
			return render_template('csvAddTeam.html')

	return render_template('csvAddTeam.html')
