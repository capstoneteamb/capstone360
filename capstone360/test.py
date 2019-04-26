import sqlite3
db = sqlite3.connect('mockup_database.db')
accessor = db.cursor()
t = ('Guy Wilson',)
#for row in accessor.execute('SELECT * FROM students WHERE name=?',t):
#	print(row)

#accessor.execute('UPDATE students SET tid = 12 WHERE name=?',t)

#for row in accessor.execute('SELECT * FROM students WHERE name=?',t):
#	print(row)

accessor.execute('SELECT MAX(id) FROM teams')
nextID = accessor.fetchone()
print(nextID[0])

t = ('Trail Blazers',)
for row in accessor.execute('SELECT * FROM teams WHERE name=?',t):
	print(row)
for row in accessor.execute('SELECT * FROM students WHERE tid=?',nextID):
	print(row)
accessor.execute('DELETE FROM teams WHERE name=?',t)
