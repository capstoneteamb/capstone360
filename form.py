# This file operates the form that students will fill out to
# complete their 360 reviews.
# It handles get and post requests for review.html.

from flask import flash, render_template, request, abort
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from datetime import datetime
import gbmodel
from catCas import validate_student
from flask_cas import login_required
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

    @login_required
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
    def get_cap(self, user_id):
        # query database to get capstone session id
        cap = 0
        try:
            student = gbmodel.students().get_student(user_id)
            # get capstone session id
            cap = student.session_id
        except SQLAlchemyError:
            self.display_error('student look up error - capstone')

        # get capstone session id
        if cap is None:
            self.display_error('No user capstone id found in database')

        return cap

    # This method returns the current user's name to display on the web page
    # input: only self
    # output: A string representing the user's name
    def get_self_name(self, user_id):
        # query database to get student
        try:
            student = gbmodel.students().get_student(user_id)
            # get name
            name = student.name
        except SQLAlchemyError:
            self.display_error('student look up error - getting their name')

        # get name
        if name is None:
            self.display_error('The user has no name')

        return name

    # This method returns the current user's team id value while testing if
    # the user exists in the database.
    # input: only self
    # output: the user's tid as an integer
    def get_tid(self, user_id):
        # get the user's team id
        tid = 0
        try:
            student = gbmodel.students().get_student(user_id)
            # get tid
            tid = student.tid
        except SQLAlchemyError:
            self.display_error('student look up error - tid')

        # get tid
        if tid is None:
            self.display_error('No user tid found in database')

        return tid

    # This method queries the database to get the user's report state. It will
    # test for any database errors.
    # input: only self
    # output: String -- The user's "active" attribute or 'Error' to indicate
    # something went wrong (could be user error, thus no need to abort)
    def get_state(self, user_id):
        try:
            student = gbmodel.students().get_student(user_id)
            # get capstone id
            cap_id = student.session_id
            # get the state based on the capstone id and the current time
            state = gbmodel.capstone_session().check_review_state(cap_id, datetime.now())
        except SQLAlchemyError:
            print('Student Look Up Error - Get State')
            return 'Error'

        # return student state
        return state

    # This method checks to ensure that the user trying to access
    #  the review exists and has an open review.
    # Input: self and user_id
    # Output: A boolean indication for
    # if the user was successfully confirmed (true) or not (false)
    def confirm_user(self, user_id):
        # check if the current user is found in the database
        # need to implement with log in

        # check the user's active reports
        state = self.get_state(user_id)
        if state == 'Error':
            return False

        student = gbmodel.students().get_student(user_id)
        if student is None:
            return False

        # depending on the user's active state, check if the user is done
        done = 0
        if state == 'midterm':
            # check if already submitted
            done = student.midterm_done
        elif state == 'final':
            # check if already submitted
            done = student.final_done
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
        # user_id = request.args.get('user_name')
        if validate_student() is False:
            return render_template('index.html')
        else:
            user_id = validate_student().id
        test_user = self.confirm_user(user_id)
        if test_user is False:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')
        # get user name
        user_name = self.get_self_name(user_id)

        # get user's team id
        tid = self.get_tid(user_id)

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
        state = self.get_state(user_id)
        if state == 'Error':
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user information.')

        # If all successful, render the page with team members and the state
        return render_template('review.html',
                               name=user_name,
                               user_id=user_id,
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
        user_id = request.form.get('user_id')
        test_user = self.confirm_user(user_id)
        if test_user is False:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')

        # get user's team id
        tid = self.get_tid(user_id)

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
        cid = self.get_cap(user_id)

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

                    if j == user_id:
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
                if i == user_id:
                    learned = request.form[('learned')]

                proud = None
                # only get 'proud' if the student is filling out final review
                if self.get_state(user_id) == 'final':
                    if i == self.user_id:
                        proud = request.form[('proud')]

                points = request.form[('points_' + str(i))]
                points = self.convert_to_int(points)

                if self.get_state(user_id) == 'midterm':
                    # for midterm set final to false
                    is_final = 0
                elif self.get_state(user_id) == 'final':
                    # for midterm set final to false
                    is_final = 1

                # add report, but do not commit yet
                test_sub = gbmodel.reports().insert_report(cid, datetime.now(), user_id,
                                                           tid, i, tech, ethic, com, coop, init,
                                                           focus, cont, lead, org, dlg, points,
                                                           strn, wkn, traits, learned, proud, is_final)
                # remember if this report submission failed
                if test_sub is False:
                    pass_insert = False

            # commit reports and update the user's state. roll back changes if insertion failed
            test_commit = gbmodel.reports().commit_reports(user_id, self.get_state(user_id), pass_insert)
            if test_commit is True:
                # success
                return render_template('submitted.html')
            else:
                self.display_error('Submission Errror')

        return render_template('review.html',
                               name=self.get_self_name(user_id),
                               mems=mems,
                               human_fields=self.human_fields,
                               code_fields=self.code_fields,
                               state=self.get_state(user_id),
                               input_error=True,
                               fatal_error=None)
