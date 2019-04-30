# This file operates the form that students will fill out to
# complete their 360 reviews.
# It handles get and post requests for review.html.

from flask import flash, render_template, request, abort
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from datetime import datetime
import gbmodel

# The review class handles get and post requests for review.html, and it
# includes helper functions for cleanliness


class review(MethodView):

    # holds fields that should appear in the table on the review page
    # -- these are what people will see
    human_fields = ['Name',
                    'Technical Mastery',
                    'Work Ethic',
                    'Communication',
                    'Cooperation',
                    'Initiative',
                    'Team Focus',
                    'Contribution',
                    'Leadership (Team Lead Only)',
                    'Organization (Team Lead Only)',
                    'Delegation (Team Lead Only)',
                    'Points',
                    'Strengths',
                    'Weaknesses',
                    'Traits to Work On']

    # holds fields that should appear in the table on the review page
    # -- this is what the form's html will use
    code_fields = ['name',
                   'tech_mast',
                   'work_ethic',
                   'comm',
                   'coop',
                   'init',
                   'team_focus',
                   'contr',
                   'lead',
                   'org',
                   'dlg',
                   'points',
                   'str',
                   'wkn',
                   'traits']

    # This will be changed to account for CAS log in
    # input: only self
    # output: the user's ID value
    def get_id(self):
        sdt_id = 0
        return sdt_id

    # If an unrecoverable error occurs and there is a need to abort,
    # report an internal server error and print the error to the console.
    # As the code indicates, this should be reserved for internal errors. User
    # error should not lead here.
    # input: self and a string to report to the console
    # output: none
    def display_error(self, err_str):
        print(err_str)
        abort(500)

    # Converts strings to integers and tests if the input was an integer.
    # User textarea input from reviews should not come into this method.
    # input: self and a number to be converted to the integer format
    # output: the same number as an integer
    def convert_to_int(self, to_convert):
        try:
            to_convert = int(to_convert)
        except ValueError:
            self.display_error('Expected integer was not a number')

        return to_convert

    # This method returns the current user's capstone session id value while
    #  testing if the user exists in the database.
    # input: only self
    # output: An integer representing the user's capstone session id
    def get_cap(self):
        # query database to get capstone session id
        cap = 0
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.get_id()).first()
        except SQLAlchemyError:
            self.display_error('student look up error - capstone')

        # get capstone session id
        cap = sdt.session_id
        if cap is None:
            self.display_error('No user capstone id found in database')

        return cap

    # This method returns the current user's name to display on the web page
    # input: only self
    # output: A string representing the user's name
    def get_self_name(self):
        # query database to get student
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.get_id()).first()
        except SQLAlchemyError:
            self.display_error('student look up error - getting their name')

        # get name
        name = sdt.name
        if name is None:
            self.display_error('The user has no name')

        return name

    # This method returns the current user's team id value while testing if
    # the user exists in the database.
    # input: only self
    # output: the user's tid as an integer
    def get_tid(self):
        # get the user's team id
        tid = 0
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.get_id()).first()
        except SQLAlchemyError:
            self.display_error('student look up error - tid')

        # get tid
        tid = sdt.tid
        if tid is None:
            self.display_error('No user tid found in database')

        return tid

    # This method queries the database to get the user's report state. It will
    # test for any database errors.
    # input: only self
    # output: String -- The user's "active" attribute or 'Error' to indicate
    # something went wrong (could be user error, thus no need to abort)
    def get_state(self):
        # query db for student's state
        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.get_id()).first()
        except SQLAlchemyError:
            print('Student Look Up Error - Get State')
            return 'Error'

        # Check if there isn't a student
        if sdt is None:
            print('Student Was None in Get State')
            return 'Error'

        # return student state
        return sdt.active

    # This method checks to ensure that the user trying to access
    #  the review exists and has an open review.
    # Input: only self
    # Output: A boolean indication for
    # if the user was successfully confirmed (true) or not (false)
    def confirm_user(self):
        # check if the current user is found in the database
        # need to implement with log in

        # check the user's active reports
        state = self.get_state()
        if state == 'Error':
            return False

        try:
            students = gbmodel.students()
            sdt = students.query.filter_by(id=self.get_id()).first()
        except SQLAlchemyError:
            self.display_error('student look up error when confirming user')

        if sdt is None:
            return False

        # depending on the user's active state, check if the user is done
        done = 0
        if state == 'midterm':
            # check if already submitted
            done = sdt.midterm_done
        elif state == 'final':
            # check if already submitted
            done = sdt.final_done
        else:
            return False

        if done == 1:
            return False

        # no errors, so return true
        return True

    # This method handles get requests to review.html.
    # Input: only self
    # Output: rendering the review.html template with given conditions --
    # team members to displate, the student's open reports state,
    # if there are any user input errors to report, and if there are
    # any fatal errors to report as a result of user action.
    def get(self):
        # check if user exists
        test_user = self.confirm_user()
        if test_user is False:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')

        # get user's team id
        tid = self.get_tid()

        # get user's team members
        try:
            mems = gbmodel.db_session.query(gbmodel.students).filter_by(tid=tid).distinct()
        except SQLAlchemyError:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user team members.')

        # get user's state of open/closed reports
        state = self.get_state()
        if state == 'Error':
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user information.')

        # If all successful, render the page with team members and the state
        return render_template('review.html',
                               mems=mems,
                               state=state,
                               human_fields=self.human_fields,
                               code_fields=self.code_fields,
                               input_error=None,
                               fatal_error=None)

    # This method handles post requests from review.html.
    # Input: only self
    # Output: rendering the review.html template with errors reported
    #  to the user or rendering the success page to indicate
        # the user was successful in submitting their reform
    def post(self):
        # check if user exists
        test_user = self.confirm_user()
        if test_user is False:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')

        # get user's team id
        tid = self.get_tid()

        # get user's team members
        try:
            mems = gbmodel.db_session.query(gbmodel.students).filter_by(tid=tid).distinct()
        except SQLAlchemyError:
            return render_template('review.html',
                                   name=self.get_self_name(),
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user team members.')

        # get student's cid
        cid = self.get_cap()

        # generate a list of the DB ids for students on the team
        id_list = []
        for mem in mems:
            if mem is not None:
                id_list.append(mem.id)

        # check points total
        total = 0
        points_pass = True

        # check that conditions for points match requirements
        for j in id_list:
            # check points for being in bounds and adding to 100
            points = request.form[('points_' + str(j))]
            try:
                try:
                    # ensure that points are all integers
                    points = int(points)
                except ValueError:
                    flash('points must be an integer')
                    points_pass = False

                if points_pass is True:
                    # add up the total points
                    total = total + points

                    if int(j) == self.get_id():
                        # make sure own score is 0
                        if points > 0 or points < 0:
                            flash('Points must be 0 for self')
                            points_pass = False
            except ValueError:
                self.display_error('Invalid input for points')

        # check that total is 100
        if total != 100:
            flash('Points total must be 100')
            points_pass = False

        # get form inputs and submit to the database
        if points_pass is True:
            for i in id_list:
                # Get each radio input and verify that it's an integer
                tech = request.form[('tech_mast_' + str(i))]
                tech = self.convert_to_int(tech)

                ethic = request.form[('work_ethic_' + str(i))]
                ethic = self.convert_to_int(ethic)

                com = request.form[('comm_' + str(i))]
                com = self.convert_to_int(com)

                coop = request.form[('coop_' + str(i))]
                coop = self.convert_to_int(coop)

                init = request.form[('init_' + str(i))]
                init = self.convert_to_int(init)

                focus = request.form[('team_focus_' + str(i))]
                focus = self.convert_to_int(focus)

                cont = request.form[('contr_' + str(i))]
                cont = self.convert_to_int(cont)

                # default leader skills to None for Null in database
                lead = None
                org = None
                dlg = None

                # check if current student is leader
                try:
                    sdt = gbmodel.students().query.filter_by(id=i).first()
                except SQLAlchemyError:
                    self.display_error('student look up error')

                if(sdt.is_lead == 1):
                    # get leader values
                    lead = request.form[('lead_' + str(i))]
                    lead = self.convert_to_int(lead)

                    org = request.form[('org_' + str(i))]
                    org = self.convert_to_int(org)

                    dlg = request.form[('dlg_' + str(i))]
                    dlg = self.convert_to_int(dlg)

                # Get string inputs
                strn = request.form[('str_' + str(i))]
                wkn = request.form[('wkn_' + str(i))]
                traits = request.form[('traits_' + str(i))]

                learned = None
                if int(i) == self.get_id():
                    learned = request.form[('learned')]

                proud = None
                # only get 'proud' if the student is filling out final review
                if self.get_state() == 'final':
                    if int(i) == self.get_id():
                        proud = request.form[('proud')]

                points = request.form[('points_' + str(i))]
                points = self.convert_to_int(points)

                if self.get_state() == 'midterm':
                    # for midterm set final to false
                    is_final = 0
                elif self.get_state() == 'final':
                    # for midterm set final to false
                    is_final = 1

                # generate the python object to use for database submission
                report = gbmodel.reports()
                report.session_id = cid
                report.time = datetime.now()
                report.reporting = self.get_id()
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

            # attempt to submit to the database
            try:
                sdt = gbmodel.db_session.query(gbmodel.students).filter_by(id=self.get_id()).first()

                if sdt is None:
                    self.display_error('user not found in database when trying to submit report')

                state = sdt.active

                # check state
                if state == 'midterm':
                    # check if already submitted
                    sdt.midterm_done = 1
                elif state == 'final':
                    # check if already submitted
                    sdt.final_done = 1
                else:
                    self.display_error('submitting reports not open')

                gbmodel.db_session.commit()
            except SQLAlchemyError:
                self.display_error('submission error')

            return render_template('submitted.html')

        return render_template('review.html',
                               name=self.get_self_name(),
                               mems=mems,
                               human_fields=self.human_fields,
                               code_fields=self.code_fields,
                               state=self.get_state(),
                               input_error=True,
                               fatal_error=None)
