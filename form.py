from flask import Blueprint, flash, g, redirect, render_template, request, url_for, abort
from sqlalchemy import Date, DateTime
from flask.views import MethodView
from datetime import datetime
import gbmodel

# forms -- both get and post handling
class review(MethodView):

    # This will be changed to account for CAS log in
    def getID(self):
        sdtID = 0
        return sdtID

    #if need to abort, report an internal server error and print the error to the console
    def displayError(self, err_str):
        print(err_str)
        abort(500)

    def convertToInt(toConvert):
        #see if input is an integer, if not display error to user
        try:
            toConvert = int(toConvert)
        except:
            displayError('input is not a number')

        return toConvert


    def getCap(self):
        # query database to get capstone session id
        cap = 0
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.getID()).first()
        except:
                displayError('student look up error - capstone')
        
        #get capstone session id
        cap = sdt.session_id
        if cap is None:
            displayError('No user capstone id found in database')

        return cap


    def getTid(self):
        #get the user's team id
        tid = 0
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.getID()).first()
        except:
                displayError('student look up error - tid')

        #get tid
        tid = sdt.tid
        if tid is None:
            displayError('No user tid found in database')

        return tid

    def getState(self):
        # query db for student's state
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.getID()).first()
        except:
            print('Student Look Up Error - Get State')
            return 'Error'
        
        #Check if there isn't a student
        if sdt is None:
            print('Student Was None in Get State')
            return 'Error'
        
        #return student state
        return sdt.active

    def confirmUser(self):
        # check if the current user is found in the database
        print('Need to confirm')
        #check the user's active reports
        state = self.getState()
        if state == 'Error':
            return False

        print('state is:' + str(state))
        students = gbmodel.students()
        sdt = students.query.filter_by(id=self.getID()).first()
        
        if sdt is None:
            return False
        
        done = 0
        if state == 'midterm':
            # check if already submitted
            done = sdt.midterm_done
        elif state == 'final':
            # check if already submitted
            done = sdt.final_done
        else:
            return False

        print('done is:' + str(done))

        if done == '1':
            return False

        #no errors, so return true
        return True

    def get(self):
        fatal_error = None
        input_error = None
        mems = None
        state = None

        #check if user exists
        test_user = self.confirmUser()
        if test_user == False:
            return render_template('review.html', mems=None, state=None, input_error = None, fatal_error='You have no open reviews.')

        #get user's team id
        tid = self.getTid()
        
        #get user's team members
        try:
            mems = gbmodel.db_session.query(gbmodel.students).filter_by(tid=tid).distinct()
        except:
            return render_template('review.html', mems=None, state=None, input_error = None, fatal_error='There was an error while retrieving user team members.')

        #get user's state of open/closed reports
        state = self.getState()
        if state == 'Error':
            return render_template('review.html', mems=None, state=None, input_error = None, fatal_error='There was an error while retrieving user information.')
        
        return render_template('review.html', mems=mems, state=state, input_error = None, fatal_error=None)

    #def post(self):

def reviewold():

    #check that the user exists, will go to error if not
    test_user = confirmUser()
    if test_user == False:
        return redirect('form/errPage/' + 'Cannot Submit Review')

    #get the user's TID
    tid = getTid()

    #get the capstone session ID
    cid = getCap()

    # get team members
    try:
        students = gbmodel.students()
        mems = gbmodel.db_session.query(gbmodel.students).join(gbmodel.team_members).filter_by(tid=tid).distinct()
    except:
        displayError('error grabbing teammates')

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

                if int(j) == self.self.getID():
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
            if int(i) == self.getID():
                learned = request.form[('learned')]

            proud = None
            #only get 'proud' if the student is filling out final review
            if getState() == 'final':
                if int(i) == self.getID():
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
            report.reporting = self.getID()
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
        #sdt = students.query.filter_by(id=self.getID()).first()
        sdt = gbmodel.db_session.query(gbmodel.students).filter_by(id=self.getID()).first()

        if sdt is None:
            displayError('user not found in database')

        state = sdt.active
        
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
