# temporary flaskr tutorial stuff for login/sqllite demo database
from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_sqlalchemy import SQLAlchemy
from .db_form import db
#from werkzeug.exceptions import abort

#from formdemo.auth import login_required
#from formdemo.db import get_db

# form blueprint
bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/midsub')
def midsub():
    return render_template('form/midsub.html')


@bp.route('/finsub')
def finsub():
    return render_template('form/finsub.html')
# This will be changed to account for CAS log in


def getID():
    id = g.user['id']
    return id


def displayError(code):
    return False


def convertToInt(toConvert):
    try:
        toConvert = int(toConvert)
    except ValueError:
        displayError(400)

    return toConvert


def getState():
    # query db
    active = db.execute(
        'SELECT s.active'
        ' FROM students s'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    state = ''
    # get value of row
    for row in state:
        if row is not None:
            state = str(row)

    return state


def confirmUser(db):
    # if the user is not found in the database, abort as internal server error
    if g.user is None:
        print('error 500')

    state = getState()
    done = ''

    if state == 'midterm':
            # check if already submitted
        done = db.execute(
            'SELECT s.midterm_done'
            ' FROM students s'
            ' WHERE s.id = ?',
            (getID(),)
        ).fetchone()
    elif state == 'final':
        # check if already submitted
        done = db.execute(
            'SELECT s.midterm_done'
            ' FROM students s'
            ' WHERE s.id = ?',
            (getID(),)
        ).fetchone()
    else:
        return False

    # get value of midterm
    for row in done:
        if row is not None:
            done = str(row)

    # get done as an int
    done = convertToInt(done)

    if done == 1:
        # error 400
        return False

    return True


def getTid(db):

    tid = 0

    # get team id from db
    res = db.execute(
        'SELECT s.tid'
        ' FROM students s'
        ' WHERE s.id = ?',
        (g.user['id'],)
    ).fetchone()

    # check if no team was found
    if res is None:
            # error 500

            # get value of team id
        for row in res:
            if row is not None:
                tid = str(row)

        # get team id as an int
        asNum = 0
        try:
            asNum = int(tid)
        except ValueError:
            # error 500
            print('500')

    return tid


def getCap(db):
    # query database to get capstone session id
    get_cid = db.execute(
        'SELECT s.session_id'
        ' FROM students s'
        ' WHERE s.id = ?',
        (g.user['id'],)
    ).fetchone()

    # get the capstone session id value
    cid = 0
    for row in get_cid:
        if row is not None:
            cid = str(row)

    # get the capstone session id as a number
    cid = convertToInt(cid)

# forms -- both get and post handling
@bp.route('/review', methods=('GET', 'POST'))
def review():
    if request.method == 'GET':
        db = get_db()  # <-- change to new db

        confirmUser(db)

        tid = getTid(db)

        if tid != 0:
            # if team found, get members from database and send to midterm form web page
            mems = db.execute(
                'SELECT DISTINCT s.name, s.id'
                ' FROM students s JOIN team_members tm ON s.tid = tm.tid'
                ' WHERE tm.tid = ?',
                (tid,)
            ).fetchall()
            state = getState()
            return render_template('form/review.html', mems=mems, state=state)

    if request.method == 'POST':
        db = get_db()  # <-- change to new db

        confirmUser(db)

        tid = getTid(db)

        cid = getCap(db)

        # get team members
        mems = db.execute(
            'SELECT DISTINCT s.id'
            ' FROM students s JOIN team_members tm ON s.tid = tm.tid'
            ' WHERE tm.tid = ?',
            (tid,)
        ).fetchall()

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
                if int(j) == int(g.user['id']):
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
                db.execute(
                    'INSERT INTO reports (time, session_id, reporting, tid, report_for, tech_mastery, work_ethic, communication, cooperation, initiative, team_focus, contribution, leadership, organization, delegation, points, strengths, weaknesses, trait_to_work_on, what_you_learned, proud_of_accomplishment, is_final)'
                    ' VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)',
                    (cid, getID(), tid, i, tech, ethic, com, coop, init, focus,
                     cont, lead, org, dlg, points, strn, wkn, traits, learned, is_final)
                )
                db.execute(
                    'UPDATE students SET midterm_done = "1"'
                    ' WHERE id = ?',
                    (getID(),)
                )
                db.commit()
            elif getState() == 'final':
                # for midterm set final to false
                is_final = 1

                # submit to database
                db.execute(
                    'INSERT INTO reports (time, session_id, reporting, tid, report_for, tech_mastery, work_ethic, communication, cooperation, initiative, team_focus, contribution, leadership, organization, delegation, points, strengths, weaknesses, trait_to_work_on, what_you_learned, proud_of_accomplishment, is_final)'
                    ' VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (cid, getID(), tid, i, tech, ethic, com, coop, init, focus,
                     cont, lead, org, dlg, points, strn, wkn, traits, learned, proud, is_final)
                )
                db.execute(
                    'UPDATE students SET final_done = "1"'
                    ' WHERE id = ?',
                    (getID(),)
                )
                db.commit()

        # send to submitted message
        return redirect('form/midsub')

# will want to get rid of with database check
@bp.route('/final', methods=('GET', 'POST'))
def finform():
    if request.method == 'GET':
        db = get_db()

        # if the user is not found in the database, abort as internal server error
        if g.user is None:
            abort(400)

        # check if already submitted
        done = db.execute(
            'SELECT s.final_done'
            ' FROM students s'
            ' WHERE s.id = ?',
            (g.user['id'],)
        ).fetchone()

        # get value of final status
        for row in done:
            if row is not None:
                done = str(row)

        # get done as an int
        isDone = 0
        try:
            isDone = int(done)
        except ValueError:
            abort(500)

        if isDone == 1:
            abort(400)

        # get team id from db
        res = db.execute(
            'SELECT s.tid'
            ' FROM students s'
            ' WHERE s.id = ?',
            (g.user['id'],)
        ).fetchone()

        # get value of team id
        for row in res:
            if row is not None:
                tid = str(row)

        # get team id as an int
        asNum = 0
        try:
            asNum = int(tid)
        except ValueError:
            abort(500)

        # check if no team was found
        if res is None:
            abort(500)
        else:
            # if team found, get members from database and send to midterm form web page
            mems = db.execute(
                'SELECT DISTINCT s.name, s.id'
                ' FROM students s JOIN team_members tm ON s.tid = tm.tid'
                ' WHERE tm.tid = ?',
                (asNum,)
            ).fetchall()
            return render_template('form/final.html', mems=mems)

    if request.method == 'POST':
        db = get_db()

        # if the user is not found in the database, abort as internal server error
        if g.user is None:
            abort(500)

        # query db to get team id
        get_tid = db.execute(
            'SELECT s.tid'
            ' FROM students s'
            ' WHERE s.id = ?',
            (g.user['id'],)
        ).fetchone()

        # check if already submitted
        done = db.execute(
            'SELECT s.final_done'
            ' FROM students s'
            ' WHERE s.id = ?',
            (g.user['id'],)
        ).fetchone()

        # get value of final status
        for row in done:
            if row is not None:
                done = str(row)

        # get done as an int
        isDone = 0
        try:
            isDone = int(done)
        except ValueError:
            abort(500)

        if isDone == 1:
            abort(400)

        # get the tid value
        for row in get_tid:
            if row is not None:
                tid = str(row)

        # get the team id as an integer
        tidAsNum = 0
        try:
            tidAsNum = int(tid)
        except ValueError:
            print(str(get_tid))

        # query database to get capstone session id
        get_cid = db.execute(
            'SELECT s.session_id'
            ' FROM students s'
            ' WHERE s.id = ?',
            (g.user['id'],)
        ).fetchone()

        # get the capstone session id value
        cid = 0
        for row in get_cid:
            if row is not None:
                cid = str(row)

        # get the capstone session id as a number
        cidAsNum = 0
        try:
            cidAsNum = int(cid)
        except ValueError:
            abort(500)

        # verify that a team was found, report internal server error if not
        if get_tid is None:
            abort(500)

        # get team members
        mems = db.execute(
            'SELECT DISTINCT s.id'
            ' FROM students s JOIN team_members tm ON s.tid = tm.tid'
            ' WHERE tm.tid = ?',
            (tidAsNum,)
        ).fetchall()

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
                if int(j) == int(g.user['id']):
                    if points != 0:
                        abort(400)
            except ValueError:
                abort(400)

        if total != 100:
            abort(400)

        for i in lst:
            # Get each radio input and verify that it's an integer, give an error if not
            tech = request.form[('tm_' + i)]
            try:
                tech = int(tech)
            except ValueError:
                abort(400)

            ethic = request.form[('we_' + i)]
            try:
                ethic = int(ethic)
            except ValueError:
                abort(400)

            com = request.form[('cm_' + i)]
            try:
                com = int(com)
            except ValueError:
                abort(400)

            coop = request.form[('co_' + i)]
            try:
                coop = int(coop)
            except ValueError:
                abort(400)

            init = request.form[('i_' + i)]
            try:
                init = int(init)
            except ValueError:
                abort(400)

            focus = request.form[('tf_' + i)]
            try:
                focus = int(focus)
            except ValueError:
                abort(400)

            cont = request.form[('cr_' + i)]
            try:
                cont = int(cont)
            except ValueError:
                abort(400)

            lead = request.form[('l_' + i)]
            try:
                lead = int(lead)
            except ValueError:
                abort(400)

            org = request.form[('o_' + i)]
            try:
                org = int(org)
            except ValueError:
                abort(400)

            dlg = request.form[('d_' + i)]
            try:
                dlg = int(dlg)
            except ValueError:
                abort(400)

            # Get string inputs
            strn = request.form[('str_' + i)]
            wkn = request.form[('wkn_' + i)]
            traits = request.form[('trait_' + i)]

            learned = ''
            if int(i) == int(g.user['id']):
                learned = request.form[('learned')]

            proud = ''
            if int(i) == int(g.user['id']):
                proud = request.form[('proud')]

            points = request.form[('points_' + i)]
            try:
                points = int(points)
            except ValueError:
                abort(400)

            # for midterm set final to false
            is_final = 1

            # submit to database
            db.execute(
                'INSERT INTO reports (time, session_id, reporting, tid, report_for, tech_mastery, work_ethic, communication, cooperation, initiative, team_focus, contribution, leadership, organization, delegation, points, strengths, weaknesses, trait_to_work_on, what_you_learned, proud_of_accomplishment, is_final)'
                ' VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (cid, g.user['id'], tid, i, tech, ethic, com, coop, init, focus,
                 cont, lead, org, dlg, points, strn, wkn, traits, learned, proud, is_final)
            )
            db.execute(
                'UPDATE students SET final_done = "1"'
                ' WHERE id = ?',
                (g.user['id'],)
            )
            db.commit()

        # send to submitted message
        return redirect('form/finsub')
