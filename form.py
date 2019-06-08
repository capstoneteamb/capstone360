"""
This file operates the form that students will fill out to
complete their 360 reviews.
It handles get and post requests for review.html.
"""

from flask import flash, render_template, request, abort
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from datetime import datetime
import gbmodel
import logging
from catCas import validate_student
from flask_cas import login_required


class review(MethodView):
    """
    The review class handles get and post requests for review.html, and it
    includes helper functions for cleanliness
    """

    # holds fields that should appear in the table on the review page
    # -- these are what people will see
    human_fields = ['Name',
                    """ Technical Mastery - Mastery of the skills
                        involved in their role(s) with the project""",
                    """ Work Ethic - Cheerfully performing their tasks
                        without excessive complaining, work avoidance""",
                    """ Communication - Ability to understand others points
                        and to effectively get their points across""",
                    """ Cooperation - Willing to be flexible, share knowledge,
                        genuinely interested in what they can do for the project to go smoothly """,
                    """ Initiative - Seeing what needs to be done and doing
                        it without someone asking them to """,
                    """ Team Focus - Interested in the entire project and its progress,
                        not just exclusively thinking about their part """,
                    "Contribution - Assess this person's overall contribution to the project",
                    'Leadership (Team Lead Only)',
                    'Organization (Team Lead Only)',
                    'Delegation (Team Lead Only)',
                    'Points - Score your teammates 0-100. Give 0 to yourself. Sum across team must be 100.',
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
    def display_error(self, err_str):
        """
        If an unrecoverable error occurs and there is a need to abort,
        report an internal server error and print the error to the console.
        As the code indicates, this should be reserved for internal errors. User
        error should not lead here.
        input: self and a string to report to the console
        output: none
        """
        logging.error("Fill Out Review - " + err_str)
        abort(500)

    def convert_to_int(self, to_convert):
        """
        Converts strings to integers and tests if the input was an integer.
        User textarea input from reviews should not come into this method.
        input: self and a number to be converted to the integer format
        output: the same number as an integer
        """
        try:
            to_convert = int(to_convert)
        except ValueError:
            self.display_error('Expected integer was not a number')

        return to_convert

    def get_self_name(self, user_id, capstone_id):
        """
        This method returns the current user's name to display on the web page
        input: only self
        output: A string representing the user's name
        """
        # query database to get student
        try:
            student = gbmodel.students().get_student_in_session(user_id, capstone_id)
            # get name
            name = student.name
        except SQLAlchemyError:
            self.display_error('student look up error - getting their name')

        # get name
        if name is None:
            self.display_error('The user has no name')

        return name

    def get_tid(self, user_id, capstone_id):
        """
        This method returns the current user's team id value while testing if
        the user exists in the database.
        input: only self
        output: the user's tid as an integer
        """
        # get the user's team id
        tid = 0
        try:
            student = gbmodel.students().get_student_in_session(user_id, capstone_id)
            # get tid
            tid = student.tid
        except SQLAlchemyError:
            self.display_error('student look up error - tid')

        # get tid
        if tid is None:
            self.display_error('No user tid found in database')

        return tid

    def get_state(self, user_id, capstone_id):
        """
        This method queries the database to get the user's report state. It will
        test for any database errors.
        input: only self
        output: String -- The user's "active" attribute or 'Error' to indicate
        something went wrong (could be user error, thus no need to abort)
        """
        try:
            # get the state based on the capstone id and the current time
            state = gbmodel.capstone_session().check_review_state(capstone_id, datetime.now())
        except SQLAlchemyError:
            logging.error('Fill Out Review - Student Look Up Error - Get State')
            return 'Error'

        # return student state
        return state

    def get_done(self, user_id, capstone_id):
        """
        check if the user is done with their review
        input: id of user to check, capstone session to check
        output: none if no result, otherwise the midterm or final done attribute of the student record
        """
        try:
            student = gbmodel.students().get_student_in_session(user_id, capstone_id)
            if student is None:
                return None

            # check the user's active reports
            state = self.get_state(user_id, capstone_id)
            if state == 'Error':
                return None

            # depending on the user's active state, check if the user is done
            done = 0
            if state == 'midterm':
                # check if already submitted
                done = student.midterm_done
            elif state == 'final':
                # check if already submitted
                done = student.final_done
            else:
                return None

            return done
        except SQLAlchemyError:
            return None

    def check_available(self, user_id, capstone_id):
        """
        This method checks if a student's reviews are open or clocked
        Inputs: user_id -- the student's id in the database,
        capstone_id -- the capstone session the student belongs to
        Outputs: True -- the student can proceed with reviews.
        False -- The student cannot proceed with reviews.
        """
        try:
            # get student
            student = gbmodel.students().get_student_in_session(user_id, capstone_id)
            if student is None:
                return False

            # check if reviews are 'open'
            if student.active == 'open':
                return True
            else:
                return False
        except SQLAlchemyError:
            return False

    def confirm_user(self, user_id, capstone_id):
        """
        This method checks to ensure that the user trying to access
        the review exists and has an open review.
        Input: self and user_id
        Output: A boolean indication for
         if the user was successfully confirmed (true) or not (false)
        """
        # check if the current user is found in the database
        student = gbmodel.students().get_student_in_session(user_id, capstone_id)
        if student is None:
            return False

        # check review availability
        available = self.check_available(user_id, capstone_id)
        if available is False:
            return False

        # check the user's active reports
        state = self.get_state(user_id, capstone_id)
        if state == 'Error':
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

        if done == 0:
            return True

        # no errors, so return true
        return True

    def get_data(self, id, capstone_id):
        """
        This method collects information of a student's submitted reviews into an object for jinja2 templating
        input: id of the student to retrieve review info for, the capstone session id to check
        output: an array of one dictionary object containing all report info in a
        style that matches review.html fields
        """
        try:
            # get student info
            tid = self.get_tid(id, capstone_id)
            state = self.get_state(id, capstone_id)
            is_final = False
            if state == 'final':
                is_final = True

            itemize = []  # will only hold dictionary
            dat = {}  # to hold all fields
            # for each report, add info to the dictionary matching the style of the review.html fields
            reports = gbmodel.reports().get_team_reports(tid, is_final)
            for report in reports:
                if report.reviewer == id:
                    dat["reviewee"] = report.reviewee
                    dat["tech_mast_" + report.reviewee] = report.tech_mastery
                    dat["work_ethic_" + report.reviewee] = report.work_ethic
                    dat["comm_" + report.reviewee] = report.communication
                    dat["coop_" + report.reviewee] = report.cooperation
                    dat["init_" + report.reviewee] = report.initiative
                    dat["team_focus_" + report.reviewee] = report.team_focus
                    dat["contr_" + report.reviewee] = report.contribution
                    dat["lead_" + report.reviewee] = report.leadership
                    dat["org_" + report.reviewee] = report.organization
                    dat["dlg_" + report.reviewee] = report.delegation
                    dat["points_" + report.reviewee] = report.points
                    dat["str_" + report.reviewee] = report.strengths
                    dat["wkn_" + report.reviewee] = report.weaknesses
                    dat["traits_" + report.reviewee] = report.traits_to_work_on
                    if report.what_you_learned is not None:
                        dat["learned"] = report.what_you_learned
                    if report.proud_of_accomplishment is not None:
                        dat["proud"] = report.proud_of_accomplishment
            itemize.append(dat)

            return itemize
        except SQLAlchemyError:
            return None

    def get(self, capstone_id):
        """
        This method handles get requests to review.html.
        Input: only self
        Output: rendering the review.html template with given conditions --
        team members to displate, the student's open reports state,
        if there are any user input errors to report, and if there are
        any fatal errors to report as a result of user action.
        """
        # check if user exists
        # user_id = request.args.get('user_name')
        if validate_student() is False:
            return render_template('index.html')
        else:
            user_id = validate_student().id
        # get user's team id
        tid = self.get_tid(user_id, capstone_id)
        # check if the user is not on the empty team (a.k.a: if the user is not on a team)
        try:
            empty_team = gbmodel.teams().get_tid_from_name("", capstone_id)
            if tid == empty_team:
                return render_template('review.html',
                                       mems=None,
                                       state=None,
                                       input_error=None,
                                       fatal_error="You aren't assigned to a team yet")
        except SQLAlchemyError:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error verifying you are on a team')

        test_user = self.confirm_user(user_id, capstone_id)
        if test_user is False:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')

        # get user name
        user_name = self.get_self_name(user_id, capstone_id)

        # get user's team members
        try:
            mems = gbmodel.students().get_team_members(tid)
        except SQLAlchemyError:
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user team members.')
        if mems is None:
            return render_template('reivew.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There are no team members to review')

        # get user's state of open/closed reports
        state = self.get_state(user_id, capstone_id)
        if state == 'Error':
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user information.')

        # for editing, check if the user is done and get their prior data
        data = self.get_data(user_id, capstone_id)
        done = self.get_done(user_id, capstone_id)
        # If all successful, render the page with team members and the state
        return render_template('review.html',
                               name=user_name,
                               user_id=user_id,
                               mems=mems,
                               state=state,
                               data=data,
                               is_done=done,
                               human_fields=self.human_fields,
                               code_fields=self.code_fields,
                               input_error=None,
                               fatal_error=None)

    def post(self, capstone_id):
        """
        This method handles post requests from review.html.
        Input: only self
        Output: rendering the review.html template with errors reported
        to the user or rendering the success page to indicate
        the user was successful in submitting their reform
        """
        # check if user exists
        user_id = request.form.get('user_id')
        test_user = self.confirm_user(user_id, capstone_id)
        if test_user is False:
            logging.error('Fill Out Review - Error when identifiyng user')
            return render_template('review.html',
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')

        # get user's team id
        tid = self.get_tid(user_id, capstone_id)
        # get users state
        state = self.get_state(user_id, capstone_id)
        if state == 'Error':
            logging.error('Fill Out Review - Error while retrieving student state')
            return render_template('review.html',
                                   name=self.get_self_name(user_id),
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='You have no open reviews.')
        # get user's team members
        try:
            mems = gbmodel.students().get_team_members(tid)
        except SQLAlchemyError:
            logging.error('Fill Out Review - Error while retrieving team members')
            return render_template('review.html',
                                   name=self.get_self_name(),
                                   mems=None,
                                   state=None,
                                   input_error=None,
                                   fatal_error='There was an error while retrieving user team members.')

        # get student's cid
        cid = capstone_id

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
            logging.info('checking points')
            # check points for being in bounds and adding to 100
            points = request.form[('points_' + str(j))]
            try:
                try:
                    # ensure that points are all integers
                    points = int(points)
                except ValueError:
                    flash('points must be an integer')
                    points_pass = False

                if points < 0:
                    flash('Points must be 0 or greater')
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

        done = self.get_done(user_id, capstone_id)
        # get form inputs and submit to the database
        if points_pass is True:
            logging.info('Retrieving Form Input')
            pass_insert = True  # will test if all insertions are successful
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
                    is_lead = gbmodel.students().check_team_lead(i, capstone_id)
                except SQLAlchemyError:
                    self.display_error('student look up error')

                if is_lead is True:
                    # get leader values
                    lead = request.form[('lead_' + str(i))]
                    lead = self.convert_to_int(lead)

                    org = request.form[('org_' + str(i))]
                    org = self.convert_to_int(org)

                    dlg = request.form[('dlg_' + str(i))]
                    dlg = self.convert_to_int(dlg)

                # Get string inputs
                strn = request.form[('str_' + str(i))]
                strn = strn.strip()
                wkn = request.form[('wkn_' + str(i))]
                wkn = wkn.strip()
                traits = request.form[('traits_' + str(i))]
                traits = traits.strip()

                learned = None
                if i == user_id:
                    learned = request.form[('learned')]
                    learned = learned.strip()
                    if len(learned) > 30000:
                        print('string too long')
                        abort(422)

                proud = None
                # only get 'proud' if the student is filling out final review
                if self.get_state(user_id, capstone_id) == 'final':
                    if i == user_id:
                        proud = request.form[('proud')]
                        proud = proud.strip()
                        if len(proud) > 30000:
                            print('string too long')
                            abort(422)

                points = request.form[('points_' + str(i))]
                points = points.strip()

                if((len(strn) > 30000) or
                   (len(wkn) > 30000) or
                   (len(traits) > 30000)):
                    print('string too long')
                    abort(422)

                points = self.convert_to_int(points)

                # default to not late
                late = False
                is_final = False
                try:
                    logging.info('Checking if Late')
                    is_not_late = gbmodel.capstone_session().check_not_late(cid,
                                                                            datetime.now(),
                                                                            self.get_state(user_id,
                                                                                           capstone_id))

                    if is_not_late is False:
                        late = True
                except SQLAlchemyError:
                    self.display_error('student look up error - capstone')

                logging.info('checking student state')

                if self.get_state(user_id, capstone_id) == 'midterm':
                    # for midterm set final to false
                    is_final = False
                elif self.get_state(user_id, capstone_id) == 'final':
                    # for midterm set final to false
                    is_final = True

                if done == 1:
                    # update existing record
                    try:
                        logging.info('updating report')
                        report = gbmodel.reports().get_report(user_id, i, tid, is_final)
                        if report is not None:
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
                        else:
                            test_sub = gbmodel.reports.insert_report(cid, datetime.now(), user_id,
                                                                     tid, i, tech, ethic, com, coop, init,
                                                                     focus, cont, lead, org, dlg, points,
                                                                     strn, wkn, traits, learned, proud,
                                                                     is_final, late)
                            if test_sub is False:
                                logging.error('report creation failure')
                                pass_insert = False

                    except SQLAlchemyError:
                        pass_insert = False
                else:
                    logging.info('creating report')
                    # insert new record
                    # add report, but do not commit yet
                    test_sub = gbmodel.reports().insert_report(cid, datetime.now(), user_id,
                                                               tid, i, tech, ethic, com, coop, init,
                                                               focus, cont, lead, org, dlg, points,
                                                               strn, wkn, traits, learned, proud,
                                                               is_final, late)
                    # remember if this report submission failed
                    if test_sub is False:
                        logging.error('report creation failure')
                        pass_insert = False

            if done == 1:
                # commit updates
                logging.info('committing edits')
                test_commit = gbmodel.reports().commit_updates(pass_insert)
            else:
                logging.info('committing reports')
                # commit reports and update the user's state.
                #  roll back changes if insertion failed
                test_commit = gbmodel.reports().commit_reports(user_id,
                                                               self.get_state(user_id, capstone_id),
                                                               capstone_id,
                                                               pass_insert)
            if test_commit is True:
                # success
                return render_template('submitted.html')
            else:
                self.display_error('Submission Error')

        return render_template('review.html',
                               name=self.get_self_name(user_id, capstone_id),
                               mems=mems,
                               human_fields=self.human_fields,
                               code_fields=self.code_fields,
                               state=self.get_state(user_id, capstone_id),
                               input_error=True,
                               fatal_error=None)
