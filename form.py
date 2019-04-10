from flask import Blueprint, flash, g, redirect, render_template, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from .db_form import db, capstone_session, teams, students, team_members, reports
from datetime import datetime


# form blueprint
bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/response')
def submission(result, mess):
    return render_template('form/response.html', success=result, mess=mess)


# This will be changed to account for CAS log in
def getID():
    sdtID = 45
    return sdtID


#only if user error can be fixed
def displayError(err_str):
    print(err_str)
    abort(400)

def convertToInt(toConvert):
    #see if input is an integer, if not display error to user

    try:
        toConvert = int(toConvert)
    except ValueError:
        displayError('input is not a number')

    return toConvert

def getState():
    # query db for student's state
    sdt = students.query.filter_by(id=getID()).first()
    if sdt is None:
        displayError('user not found in database')
    state = sdt.active
    
    return state

def confirmUser():
    # check if the current user is found in the database

    # if g.user is None: needs login
        #error

    #check the user's active reports
    state = getState() 
    done = ''

    sdt = students.query.filter_by(id=getID()).first()
    if sdt is None:
        displayError('user not found in database')
    if state == 'midterm':
        # check if already submitted
        done = sdt.midterm_done
    elif state == 'final':
         # check if already submitted
        done = sdt.final_done
    else:
        displayError('submitting reports not open')

    # get done as an int
    done = convertToInt(done)

    if done == 1:
        displayError('Reviews already submitted')


def getTid():
    #get the user's team id
    tid = 0
    sdt = students.query.filter_by(id=getID()).first()
    tid = sdt.tid
    if tid is None:
        displayError('user not found in database')
    return tid

def getCap():
    # query database to get capstone session id
    cap = 0
    sdt = students.query.filter_by(id=getID()).first()
    cap = sdt.session_id
    if cap is None:
        displayError('user not found in database')

    return cap

# forms -- both get and post handling
@bp.route('/review', methods=('GET', 'POST'))
def review():
    if request.method == 'GET':
        #check if user exists
        confirmUser()

        #get user's team id
        tid = getTid()

        if tid != 0:
            # if team found, get members from database and send to midterm form web page

            sdt = students.query.join(team_members).filter_by(tid=tid).distinct()
            state = getState()
            return render_template('form/review.html', mems=sdt, state=state)

    if request.method == 'POST':

        #check that the user exists, will go to error if not
        confirmUser()

        #get the user's TID
        tid = getTid()

        #get the capstone session ID
        cid = getCap()

        # get team members
        mems = students.query.join(team_members).filter_by(tid=tid).distinct()

        # add members' ids to a list
        lst = []
        for mem in mems:
            if mem is not None:
                id = mem.id
                lst.append(id)
                
        # check points total
        total = 0
        pointsPass = True

        for j in lst:
            #check points for being in bounds and adding to 100
            points = request.form[('points_' + j)]
            try:
                points = convertToInt(points)
                total = total + points
                if int(j) == getID():
                    #make sure own score is 0
                    if points > 0 or points < 0:
                        flash('Points must be 0 for self')
                        pointsPass = False
            except ValueError:
                displayError('Invalid input for points')

        if total != 100:
            flash('Points total must be 100')
            pointsPass = False

        if pointsPass == True:
            for i in lst:
                # Get each radio input and verify that it's an integer, give an error if not
                print(i)
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

                #default leader skills to None for Null
                lead = None
                org = None
                dlg = None

                #check if current student is leader
                sdt = students.query.filter_by(id=i).first()
                if(sdt.is_lead == 1):
                    #get leader values
                    lead = request.form[('l_' + i)]
                    lead = convertToInt(lead)

                    org = request.form[('o_' + i)]
                    org = convertToInt(org)

                    dlg = request.form[('d_' + i)]
                    dlg = convertToInt(dlg)

                
                # Get string inputs
                strn = request.form[('str_' + i)]
                wkn = request.form[('wkn_' + i)]
                traits = request.form[('trait_' + i)]

                learned = None
                if int(i) == getID():
                    learned = request.form[('learned')]

                proud = None
                #only get 'proud' if the student is filling out final review
                if getState() == 'final':
                    if int(i) == getID():
                        proud = request.form[('proud')]

                points = request.form[('points_' + i)]
                points = convertToInt(points)

                if getState() == 'midterm':
                    # for midterm set final to false
                    is_final = 0
                elif getState() == 'final':
                    # for midterm set final to false
                    is_final = 1

                
                report = reports()
                report.session_id = cid
                report.time = datetime.now()
                report.reporting = getID()
                report.tid = tid
                report.report_for = i
                report.tech_mastery = tech
                report.work_ethic = ethic
                report.communication = com
                report.cooperation = coop
                report.initiative = init
                report.team_focus = focus
                report.contribution = cont
                report.leadership = lead
                report.organization = org
                report.delegation = dlg
                report.points = points
                report.strengths = strn
                report.weaknesses = wkn
                report.traits_to_work_on = traits
                report.what_you_learned = learned
                report.proud_of_accomplishment = proud
                report.is_final = is_final
                
                db.session.add(report)
                db.session.commit()
                

            # send to submitted message
            return redirect('form/response', success=True, mess='Review Submitted')
        return redirect(request.url)
