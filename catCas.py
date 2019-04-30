import gbmodel
import datetime
from flask_cas import CAS

# function to grab cas username and passes the value to gbmmodel to vaidate


def validate():
    session = gbmodel.capstone_session()

    currentDate = datetime.datetime.now()
    month = int(currentDate.month)
    year = currentDate.year
    if month in range(9, 11):
        term = "Fall"
    elif month in range(3, 5):
        term = "Spring"
    elif month in range(6, 8):
        term = "Summer"
    else:
        term = "Winter"

    # get current capstone session id
    sessionID = session.get_session_id(term, year)

    cas = CAS()
    username = cas.username
    students = gbmodel.students()
    found_sessionID = students.validate(username)
    

    # check to see if student's session_id is the current capstone session id
    # if not then check if they are in the 2nd half of their capstone session
    if found_sessionID == -1:
        return False
    elif found_sessionID == sessionID:
        return True
    elif (1 + found_sessionID) == sessionID:
        return True
    return False
