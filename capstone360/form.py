#form.py
#this file is used to set up the backend for students receiving, filling out, and submitting their reviews
from flask import(
    Blueprint, g, redirect, render_template, request, url_for
)

# form blueprint
bp = Blueprint('form', __name__, url_prefix='/form')


#This will be changed to account for CAS log in
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
    #query db
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
            #error 500
        
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
            #error 400
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
            #error 500

        # get value of team id
        for row in res:
            if row is not None:
                tid = str(row)

        # get team id as an int
        asNum = 0
        try:
            asNum = int(tid)
        except ValueError:
            #error 500
    
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

#midterm complete message page
@bp.route('/midsub')
def midsub():
    return render_template('form/midsub.html')

#final complete message page
@bp.route('/finsub')
def finsub():
    return render_template('form/finsub.html')

#forms -- both get and post handling
@bp.route('/review', methods=('GET', 'POST'))
def review():
    if request.method == 'GET':
        db = get_db() #<-- change to new db

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
        db = get_db() #<-- change to new db

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
                        #error 400
            except ValueError:
                #error 400

        if total != 100:
            #error 400

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