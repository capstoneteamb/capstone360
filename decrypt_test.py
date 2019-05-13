import gbmodel
from cryptography.fernet import Fernet

key_file = open('key.txt')
key = key_file.readline()
key = bytes(key.encode("UTF8"))
cipher = Fernet(key)

students = gbmodel.students()
'''  # Decerypt and print all students
c_names = students.query.all()
for each in c_names:
  p_name = cipher.decrypt(each.name)
  p_name = p_name.decode('UTF8')
  print(p_name)
'''
#  Decrypt and print students in session 0 team 0
print("Team 0:")
print(students.get_students(0, 0))

'''
#  Insert a student to the database, then decrypt and print the team with the new student
students.insert_student("Dame Dolla", "Letter0@blazers.com", 1990, 0, "Team 0")
print("Team 0:")
print(students.get_students(0, 0))
'''
print(cipher.encrypt(bytes("cclev2", encoding='UTF8')))
print(students.validate("cclev2"))
