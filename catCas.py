import gbmodel
from flask_cas import CAS


def validate_student():
    """
    function to grab cas username and passes the value to gbmmodel to vaidate
    INPUT: none
    OUTPUT: return False if the id does not exist
            return student infomation otherwise
    """
    cas = CAS()
    username = cas.username
    students = gbmodel.students()
    found_student = students.validate(username)
    if found_student is False:
        return False
    return found_student


def validate_professor():
    """
    check to see if professor id is in the professor table
    INPUT: none
    OUTPUT: return False if the id does not exist
            return True otherwise
    """
    cas = CAS()
    username = cas.username
    professors = gbmodel.professors()
    found_professors = professors.get_professor(username)
    if not found_professors:
        return False
    return found_professors
