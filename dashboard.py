import datetime
import gbmodel
import catCas
# note: waiting for updated code to run through flake8


def get():
    if catCas.validate() is False:
        return False
    """
    get data from model
    """
    current_date = datetime.datetime.now()
    month = int(current_date.month)

    year = current_date.year
    if month in range(9, 11):
        term = "Fall"
    elif month in range(3, 5):
        term = "Spring"
    elif month in range(6, 8):
        term = "Summer"
    else:
        term = "Winter"
    session = gbmodel.capstone_session()
    team = gbmodel.teams()
    student = gbmodel.students()

    # What if we don't have any session for this year/term?
    session_id = session.get_session_id(term, year)
    tids = [row[0] for row in team.get_team_session_id(session_id)]
    team_names = [row[2] for row in team.get_team_session_id(session_id)]
    lists = [[] for _ in range(len(tids))]

    for i in range(len(tids)):
        names = student.get_students(tids[i], session_id)
        temp = [team_names[i]]
        for name in names:
            temp.append(name[0])
        lists[i] = (temp, tids[i], session_id)
    return lists 
