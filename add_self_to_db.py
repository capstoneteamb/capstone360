import gbmodel
from cryptography.fernet import Fernet

key_file = open('key.txt')
key = key_file.readline()
key = bytes(key.encode("UTF8"))
cipher = Fernet(key)

students = gbmodel.students()

students.insert_student("cclev2", "cclev2@pdx.edu", "9000", 0, "Team 0")
