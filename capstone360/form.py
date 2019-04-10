from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_sqlalchemy import SQLAlchemy
from .db_form import db, capstone_session, teams, students, team_members
#from werkzeug.exceptions import abort

# form blueprint
bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/midsub')
def submission():
    return render_template('form/submission.html')


# This will be changed to account for CAS log in
def getID():
    id = 45
    return id


def displayError(code):
    print(code(str))


def convertToInt(toConvert):
    try:
        toConvert = int(toConvert)
    except ValueError:
        displayError(400)

    return toConvert


def getState():
    # query db
    sdt = students.query.filter_by(id=getID()).first()
    if sdt is None:
        displayError(500)
    state = sdt.active
    
    return state


def confirmUser():
    # if the user is not found in the database, abort as internal server error

    # if g.user is None: needs login
        #print('error 500')

    state = getState()
    done = ''

    sdt = students.query.filter_by(id=getID()).first()
    if sdt is None:
        displayError(500)
    if state == 'midterm':
        # check if already submitted
        done = sdt.midterm_done
    elif state == 'final':
         # check if already submitted
        done = sdt.final_done
    else:
        return False

    # get done as an int
    done = convertToInt(done)

    if done == 1:
        # error 400
        return False

    return True


def getTid():
    tid = 0
    sdt = students.query.filter_by(id=getID()).first()
    tid = sdt.tid
    if tid is None:
        displayError(500)
    return tid


def getCap():
    # query database to get capstone session id
    cap = 0
    sdt = students.query.filter_by(id=getID()).first()
    cap = sdt.session_id
    if tid is None:
        displayError(500)

    return cap

# forms -- both get and post handling
@bp.route('/review', methods=('GET', 'POST'))
def review():
    if request.method == 'GET':
        # db = get_db()  # <-- change to new db

        confirmUser()

        tid = getTid()

        if tid != 0:
            # if team found, get members from database and send to midterm form web page

            sdt = students.query.join(team_members).filter_by(tid=tid).distinct()
            state = getState()
            return render_template('form/review.html', mems=sdt, state=state)

    if request.method == 'POST':

        confirmUser()

        tid = getTid()

        cid = getCap()

        # get team members
        mems = students.query.filter_by(id=getID()).join(team_members).filter_by(tid=tid).distinct()

        # add members to a list
        lst = []
        for mem in mems:
            if mem is not None:
                lst.append(mem['id'])

        # check points total
        total = 0
        for j in lst:
            points = request.form[('points_' + j)]
            try:
                points = int(points)
                total = total + points
                if int(j) == getID():
                    if points > 0 or points < 0:
                        # error 400
                        print('400')
            except ValueError:
                # error 400
                print('400')

        if total != 100:
            # error 400
            print('400')

        for i in lst:
            # Get each radio input and verify that it's an integer, give an error if not
            tech = request.form[('tm_' + i)]
            tech = convertToInt(tech)

            ethic = request.form[('we_' + i)]
            ethic = convertToInt(ethic)

            com = request.form[('cm_' + i)]
            com = convertToInt(com)

            coop = request.form[('co_' + i)]
            coop = convertToInt(coop)

            init = request.form[('i_' + i)]
            init = convertToInt(init)

            focus = request.form[('tf_' + i)]
            focus = convertToInt(focus)

            cont = request.form[('cr_' + i)]
            cont = convertToInt(cont)

            lead = request.form[('l_' + i)]
            lead = convertToInt(cont)

            org = request.form[('o_' + i)]
            org = convertToInt(org)

            dlg = request.form[('d_' + i)]
            dlg = convertToInt(dlg)

            # Get string inputs
            strn = request.form[('str_' + i)]
            wkn = request.form[('wkn_' + i)]
            traits = request.form[('trait_' + i)]

            learned = ''
            if int(i) == int(g.user['id']):
                learned = request.form[('learned')]

            proud = ''
            if getState() == 'final':
                if int(i) == int(g.user['id']):
                    proud = request.form[('proud')]

            points = request.form[('points_' + i)]
            points = convertToInt(points)

            if getState() == 'midterm':
                # for midterm set final to false
                is_final = 0
                # submit to database
                #db.execute(
                #    'INSERT INTO reports (time, session_id, reporting, tid, report_for, tech_mastery, work_ethic, communication, cooperation, initiative, team_focus, contribution, leadership, organization, delegation, points, strengths, weaknesses, trait_to_work_on, what_you_learned, proud_of_accomplishment, is_final)'
                #    ' VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)',
                #    (cid, getID(), tid, i, tech, ethic, com, coop, init, focus,
                #     cont, lead, org, dlg, points, strn, wkn, traits, learned, is_final)
                #)
                #db.execute(
                #    'UPDATE students SET midterm_done = "1"'
                #    ' WHERE id = ?',
                #    (getID(),)
                #)
                #db.commit()
            elif getState() == 'final':
                # for midterm set final to false
                is_final = 1

                # submit to database
                #db.execute(
                 #   'INSERT INTO reports (time, session_id, reporting, tid, report_for, tech_mastery, work_ethic, communication, cooperation, initiative, team_focus, contribution, leadership, organization, delegation, points, strengths, weaknesses, trait_to_work_on, what_you_learned, proud_of_accomplishment, is_final)'
                  #  ' VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   # (cid, getID(), tid, i, tech, ethic, com, coop, init, focus,
                    # cont, lead, org, dlg, points, strn, wkn, traits, learned, proud, is_final)
                #)
                #db.execute(
                 #   'UPDATE students SET final_done = "1"'
                  #  ' WHERE id = ?',
                   # (getID(),)
                #)
                #db.commit()

        # send to submitted message
        return redirect('form/midsub')
