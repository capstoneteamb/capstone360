from cryptography.fernet import Fernet
import gbmodel
id = raw_input("Professor's id")
name = raw_input("Professor's name(first last)")
table = gbmodel.professors()
table.insert_professor(name, id)
