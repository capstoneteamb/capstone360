import os
import sqlite3
import io
import csv
from flask import Flask, render_template, request, g
app = Flask(__name__)

@app.route("/addTeam", methods=['GET', 'POST'])
def addTeam():
	#Database variables
	db = sqlite3.connect('mockup_database.db') # Connect to the database
	accessor = db.cursor() # This is used to access the database
	if request.method == 'POST':
		teamName = request.form['Team Name']
		#Let s represent a single student
		s1 = request.form['student1']
		s2 = request.form['student2']
		s3 = request.form['student3']
		s4 = request.form['student4']
		s5 = request.form['student5']
		s6 = request.form['student6']
		s7 = request.form['student7']
		s8 = request.form['student8']
		students = [s1, s2, s3, s4, s5, s6, s7, s8] # An array containing all students
		
		accessor.execute('SELECT MAX(id) FROM teams') # Find the highest ID value in the team table
		nextID = 1+accessor.fetchone()[0] # Get the next unique ID value
		accessor.execute('INSERT INTO teams VALUES(?,?,?)',
			 							(nextID,0,teamName)) 

		for s in students:
			accessor.execute('UPDATE students SET tid = ? where name=?',(nextID, s))

		#accessor.execute('UPDATE students SET tid = ? WHERE name=?',(nextID,student1))
		db.commit()
		db.close()
		return render_template('addTeam.html')

	return render_template('addTeam.html')

@app.route("/csvAddTeam", methods=['GET', 'POST'])
def csvAddTeam():
	#Database variables
	db = sqlite3.connect('mockup_database.db') # Connect to the database
	accessor = db.cursor() # This is used to access the database
	if request.method == 'POST':
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
			accessor.execute('SELECT MAX(id) FROM teams') # Find the highest ID value in the team table
			nextID = 1+accessor.fetchone()[0] # Get the next unique ID value
			accessor.execute('INSERT INTO teams VALUES(?,?,?)',
											(nextID,0,teamName)) 

			for s in students:
				accessor.execute('UPDATE students SET tid = ? where name=?',(nextID, s)) 

			db.commit()
			db.close()
			return render_template('csvAddTeam.html')

	return render_template('csvAddTeam.html')
