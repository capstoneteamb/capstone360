import gbmodel
import datetime
from flask_cas import CAS

# function to grab cas username and passes the value to gbmmodel to vaidate
# check to see if student id is in the current session
# INPUT: none
# OUTPUT: return False if the id does not exist
#         return student infomation otherwise


def validate_student():
    session = gbmodel.capstone_session()

    currentDate = datetime.datetime.now()
    month = int(currentDate.month)
    year = currentDate.year
    if month in range(9, 11):
        term = "Fall"
    elif month in range(3, 6):
        term = "Spring"
    elif month in range(6, 9):
        term = "Summer"
    else:
        term = "Winter"

    # get current capstone session id
    session_id = session.get_session_id(term, year)
    cas = CAS()
    username = cas.username
    students = gbmodel.students()
    found_student = students.validate(username)
    # check to see if student's session_id is the current capstone session id
    # if not then check if they are in the 2nd half of their capstone session
    if found_student is False:
        return False
    elif found_student.session_id == session_id:
        return found_student
    elif (1 + found_student.session_id) == session_id:
        return found_student
    return False

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
    return True
