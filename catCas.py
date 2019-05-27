import gbmodel
from flask_cas import CAS

# function to grab cas username and passes the value to gbmmodel to vaidate
# INPUT: none
# OUTPUT: return False if the id does not exist
#         return student infomation otherwise


def validate_student():
    cas = CAS()
    username = cas.username
    students = gbmodel.students()
    found_student = students.validate(username)
    # check to see if student's session_id is the current capstone session id
    # if not then check if they are in the 2nd half of their capstone session
    if found_student is False:
        return False
    return found_student

# check to see if professor id is in the professor table
# INPUT: none
# OUTPUT: return False if the id does not exist
#         return True otherwise


def validate_professor():
    cas = CAS()
    username = cas.username
    professors = gbmodel.professors()
    found_professors = professors.get_professors(username)
    if not found_professors:
        return False
    return found_professors
