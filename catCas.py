import gbmodel
from app import cas

def validate():
    username = cas.username
    students = gbmodel.students()
    found = students.validate(username)
    print(found," in validate")
    if found is None:
        return False
    return True