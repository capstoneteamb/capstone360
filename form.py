from flask import Blueprint, flash, g, redirect, render_template, request, url_for, abort
from sqlalchemy import Date, DateTime
from datetime import datetime
import gbmodel

# form blueprint
form_bp = Blueprint('form', __name__, url_prefix='/form')

#for successful response
@form_bp.route('/response')
def submission():
    return render_template('form/response.html')

#for some errors, redirect user away from form
@form_bp.route('/errPage/<err_msg>')
def errPage(err_msg):
    return render_template("form/errPage.html", msg = err_msg)

# This will be changed to account for CAS log in
def getID():
    sdtID = 0
    return sdtID

#if need to abort
def displayError(err_str):
    print(err_str)
    abort(500)

def convertToInt(toConvert):
    #see if input is an integer, if not display error to user
    try:
        toConvert = int(toConvert)
    except:
        displayError('input is not a number')

    return toConvert

def getState():
    # query db for student's state
    try:
        students = gbmodel.students()
        sdt = students.query.filter_by(id=getID()).first()
    except:
        displayError('student look up error - state')
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

    students = gbmodel.students()
    sdt = students.query.filter_by(id=getID()).first()
    if sdt is None:
        return False
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
        return False

    return True


def getTid():
    #get the user's team id
    tid = 0
    try:
        students = gbmodel.students()
        sdt = students.query.filter_by(id=getID()).first()
    except:
            displayError('student look up error -tid')
    tid = sdt.tid
    if tid is None:
        displayError('user not found in database')
    return tid

def getCap():
    # query database to get capstone session id
    cap = 0
    try:
        students = gbmodel.students()
        sdt = students.query.filter_by(id=getID()).first()
    except:
            displayError('student look up error - capstone')
    cap = sdt.session_id
    if cap is None:
        displayError('user not found in database')

    return cap

# forms -- both get and post handling
@form_bp.route('/review', methods=('GET', 'POST'))
def review():
    if request.method == 'GET':
        #check if user exists
        test_user = confirmUser()
        if test_user == False:
            return redirect('form/errPage/' + 'No Accessible Review')

        #get user's team id
        tid = getTid()
        # if team found, get members from database and send to midterm form web page
        try:
            sdt = gbmodel.db_session.query(gbmodel.students).join(gbmodel.team_members).filter_by(tid=tid).distinct()
        except:
            displayError('student look up error - review')
        state = getState()
        return render_template('form/review.html', mems=sdt, state=state)

    if request.method == 'POST':

        #check that the user exists, will go to error if not
        test_user = confirmUser()
        if test_user == False:
            return redirect('form/errPage/' + 'Cannot Submit Review')

        #get the user's TID
        tid = getTid()

        #get the capstone session ID
        cid = getCap()

        # get team members
        students = gbmodel.students()
        mems = gbmodel.db_session.query(gbmodel.students).join(gbmodel.team_members).filter_by(tid=tid).distinct()

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
            points = request.form[('points_' + str(j))]
            try:
                try:
                    points = int(points)
                except ValueError:
                    flash('points must be an integer')
                    pointsPass = False

                if pointsPass == True:
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
                tech = request.form[('tm_' + str(i))]
                tech = convertToInt(tech)

                ethic = request.form[('we_' + str(i))]
                ethic = convertToInt(ethic)

                com = request.form[('cm_' + str(i))]
                com = convertToInt(com)

                coop = request.form[('co_' + str(i))]
                coop = convertToInt(coop)

                init = request.form[('i_' + str(i))]
                init = convertToInt(init)

                focus = request.form[('tf_' + str(i))]
                focus = convertToInt(focus)

                cont = request.form[('cr_' + str(i))]
                cont = convertToInt(cont)

                #default leader skills to None for Null
                lead = None
                org = None
                dlg = None

                #check if current student is leader
                try:
                    sdt = students.query.filter_by(id=i).first()
                except:
                    displayError('student look up error')

                if(sdt.is_lead == 1):
                    #get leader values
                    lead = request.form[('l_' + str(i))]
                    lead = convertToInt(lead)

                    org = request.form[('o_' + str(i))]
                    org = convertToInt(org)

                    dlg = request.form[('d_' + str(i))]
                    dlg = convertToInt(dlg)

                
                # Get string inputs
                strn = request.form[('str_' + str(i))]
                wkn = request.form[('wkn_' + str(i))]
                traits = request.form[('trait_' + str(i))]

                learned = None
                if int(i) == getID():
                    learned = request.form[('learned')]

                proud = None
                #only get 'proud' if the student is filling out final review
                if getState() == 'final':
                    if int(i) == getID():
                        proud = request.form[('proud')]

                points = request.form[('points_' + str(i))]
                points = convertToInt(points)

                if getState() == 'midterm':
                    # for midterm set final to false
                    is_final = 0
                elif getState() == 'final':
                    # for midterm set final to false
                    is_final = 1

                report = gbmodel.reports()
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
                
                gbmodel.db_session.add(report)

        try:
            #students = gbmodel.students()
            #sdt = students.query.filter_by(id=getID()).first()
            sdt = gbmodel.db_session.query(gbmodel.students).filter_by(id=getID()).first()
            state = sdt.active
            if sdt is None:
                displayError('user not found in database')
            if state == 'midterm':
                # check if already submitted
                print('student id' + str(sdt.id))
                sdt.midterm_done = 1
            elif state == 'final':
                # check if already submitted
                sdt.final_done = 1
            else:
                displayError('submitting reports not open')

            gbmodel.db_session.commit()
        except:
            displayError('submission error')
                
        return redirect('form/response')
