from capstone360.gbmodel import gbmodel
from cryptography.fernet import Fernet

cipher = Fernet(b'FbR9YKJHJGqXzGSrqY9Fjlz_6_IQFd3fNM823uD24_o=')

students = gbmodel.students()
'''
c_names = students.query.all()
for each in c_names:
  p_name = cipher.decrypt(each.name)
  p_name = p_name.decode('UTF8')
  print(p_name)
'''

print("Team 0:")
print(students.get_students(0, 0))

students.insert_student("Dame Dolla", 1990, 0, "Team 0")
print("Team 0:")
print(students.get_students(0, 0))

