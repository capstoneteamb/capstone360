# Classes Summary

## form. py
##### class review
The review class handles get and post requests for reivew.html, and it includes helper functions for cleanliness
Uses variables human_fields and code_fields to populate the review form and its html structure

display_error(self, err_str):<br>
If an unrecoverable error occurs and there is a need to abort,
report an internal server error and print the error to the console.
As the code indicates, this should be reserved for internal errors. User
error should not lead here.
input: self and a string to report to the console
output: none

convert_to_int(self, to_convert):<br>
Converts strings to integers and tests if the input was an integer.
User textarea input from reviews should not come into this method.
input: self and a number to be converted to the integer format
output: the same number as an integer

get_self_name(self, user_id, capstone_id):<br>
This method returns the current user's name to display on the web page
input: only self
output: A string representing the user's name

get_tid(self, user_id, capstone_id):<br>
This method returns the current user's team id value while testing if
the user exists in the database.
input: only self
output: the user's tid as an integer

get_state(self, user_id, capstone_id):<br>
This method queries the database to get the user's report state. It will
test for any database errors.
input: only self
output: String -- The user's "active" attribute or 'Error' to indicate
something went wrong (could be user error, thus no need to abort)  

get_done(self, user_id, capstone_id):<br>
check if the user is done with their review
input: id of user to check, capstone session to check
output: none if no result, otherwise the midterm or final done attribute of the student record

check_available(self, user_id, capstone_id):<br>
This method checks if a student's reviews are open or clocked
Inputs: user_id -- the student's id in the database,
capstone_id -- the capstone session the student belongs to
Outputs: True -- the student can proceed with reviews.
False -- The student cannot proceed with reviews.
         
confirm_user(self, user_id, capstone_id):<br>
This method checks to ensure that the user trying to access
the review exists and has an open review.
Input: self and user_id
Output: A boolean indication for if the user was successfully confirmed (true) or not (false)

get_data(self, id, capstone_id):<br>
This method collects information of a student's submitted reviews into an object for jinja2 templating
input: id of the student to retrieve review info for, the capstone session id to check
output: an array of one dictionary object containing all report info in a
style that matches review.html fields

get(self, capstone_id):<br>
This method handles get requests to review.html.
Input: Self and the capstone session id for the review.
Output: rendering the review.html template with given conditions --
team members to display, the student's open reports state,
if there are any user input errors to report, and if there are
any fatal errors to report as a result of user action. 
This also handles editing, in which case review data will be included in the output as well.

post(self, capstone_id):<br>
This method handles post requests from review.html.
Input: only self and the capstone session id of the capstone session reviews are being turned in for
Output: rendering the review.html template with errors reported
to the user or rendering the success page to indicate
the user was successful in submitting their reform

## index. py

##### class Index
This class handles the get request for index.html

## prof_dashboard.py

##### class ProfDashboard
ProfDashboard class handles get and post requests for profDashboard.html

valid_email(self, email):<br>
Verify if the email is in a correct syntax by checking if it has '@' & '.'
Input: self and new email
Output: return True if it matches the format, False otherwise

get(self):<br>
Get session_id from the previous selected session
If None returned then request for a selection.
Otherwise, display the current session_id

post(self):<br>
This method handles all the functionalities from proDashboard includes 
- add/remove students/teams
- add/remove session
- set review midterm/final start/end dates
- setting reviews to be open/closed,
- set team lead
- import students from csv files
- assign team for unassigned students

##### class AddStudent
This class handles get request for addStudent.html

get(self):<br>
This method handles get requests go addStudent.html
Input: only self
Output: rendering the addSession.html template with session id
name of the team from profDashboard.html

##### class AddSession
This class handles get requests for addSession.html

get(self):<br>
This method handles get requests go addSession.html
Input: only self
Output: rendering the addSession.html template with session id
from profDashboard.html

##### class RemoveSession
This class handles get requests for removeSession.html

get(self):<br>
This method handles get requests go removeSession.html
Input: only self
Output: rendering the removeSession.html template with session id
from profDasboard.html

##### class AddTeam
This class handles get requests for addTeam.html

get(self):<br>
This method handles get requests go addTeam.html
Input: only self
Output: rendering the addSession.html template with session id
from profDashboard.html

##### class AddTeamCSV
This class handles import students via CSV file

##### class RemoveTeam
This class handles get requests for removeTeam.html

get(self):<br>
This method handles get requests go removeTeam.html
Input: only self
Output: rendering the addSession.html template with session id
and team name from profDashboard.html

##### class SetDate
This class handles get requests for setDate.html

get(self):<br>
This method handles get requests go setDate.html
Input: only self
Output: rendering the addSession.html template with session id
from profDashboard.html

##### class AssignTeam
This class handles team assignment for assignTeam.html

get(self): <br>
Input: only self
Output: rendering the assignTeam.html template with list of unassigned students,
        list of sessions, session id for current session and error message

## report. py

##### class MissingStudentException
Exception class to raise exception if no students for a given team or session are found

##### class MissingTeamException
Exception class to raise exception if no team is in the database when searched

##### class GeneratedProfessorReportView
Generates a report for a specific student, for viewing by a professor.

get(self)<br>
Input: only self
Generates a report for a specific student, for viewing by a professor.
Specifically, generates a single report, for a single session and term (midterm or final), for a
single student, with comments deanonymized.

##### class GeneratedAnonymousReportView
Generates all anonymized reports for printing and handing out to students.


_make_printable_reports(session_id, is_final): <br>
Compiles all reports for a session into one for printing.
This means we generate a bunch of anonymized reports, then concatenate them, since page breaks are
handled in the HTML template.

Keyword arguments:
session_id -- session to generate reports for
is_final -- if True, makes a final report. If False, generates a midterm report.


_make_student_report_pdf(student_id, session_id, is_final, is_professor_report=False):
Renders a report for a student, defaulting to the results of their midterm review.
Unless is_professor_report is set to True, the report will be anonymized.

Keyword arguments:
student_id -- id of the student to generate a report for
session_id -- session to generate reports for
is_final -- if True, makes a final report. If False, generates a midterm report.
is_professor_report -- if True, makes a deanonymized report. If False, generates an anonymous report.

## student_dashboard.py

##### class StudentDashboard
Student Dashboard class handles get requests from index.html when student login button is clicked on.\

valid_email(self, email): <br>
Verify if the new email is in a correct syntax
by checking if it has '@' and '.'
Input: self and new email
Output: return True if it matches the format, False otherwise

get(self):<br>
This method handles get requests to studentDashboard.html
Input: only self
Output: return to index.html if the student id is not in the student
        table, rendering the studentDashboard.html template

post(self):<br>
This method handles post request from editStudent.html
Input: only self
Output: prompt to the user error message if the inputs are invalid
        Add new info to the database and return to studentDashboard.html

##### class EditStudent
Edit Student class handles get requests from student Dashboard when Edit is clicked on

get(self):<br>
This method handles get request from studentDashboard.html
Input: only self
Output: return to editStudent.html


## student_register.py

##### class StudentRegister
Facilitates the rendering and processing of the register student page, which allows students to register for a currently ongoing capstone session

display_error(self, error_msg):<br>
Returns an error-page rendering of studentRegister.html that displays the given error_msg
Input: self, error_msg
Output: the error-page rendering of the studentRegister.html template

get(self):<br>
Processes student register class GET requests. More specifically, it loads a form that a student (once
logged in) can fill out and submit in order to register for an active Capstone session.
Input: self
Output: a rendering of the student register page: featuring a student registration form if everything
        went well, or an error message if something went wrong

post(self):<br>
Handles student registration requests, which come in the form of POST requests submitted via the form
that is generated in GET requests
Input: self
Output: a rendering of the student register page: with a success message and link to the student
        dashboard if everything went well, or with an error message if there was a problem

## view_register.py

##### class ViewReview
A method view class that oversees the viewing of individual student reviews

interperate_rating(self, rating):<br>
A function to add a (or some) descriptor word(s) to flush out the numerical ratings we store as
answers to most of our review questions
INPUT: -self (a reference to the instance of the class the function is being called on?),
        -rating (the numerical rating that we will flush out)
OUTPUT: a string containing the numerical rating and the descriptor text

display_error(self, error):<br>
Prints a given error message to the console and return a rendering of the viewReview.html page with
a generic error message in it
INPUT: -self,
        -error (the error we wil to print to the console)
OUTPUT: an error page rendering of the viewReview template

post(self):<br>
Determines how the class will handle POST requests
INPUT: self
OUTPUT: It looks like it will return a rendering of the viewReview.html file. The information
        included in this rendering depends on the POST request parameters.

## view_student.py

##### class ViewStudent
A class for the student page (that a professor would access from the professor dashboard. The professor should be able to use this page to access the midterm and final reviews for a student.)

check_review_done(self, reviews_table, reviewer_id, reviewee_id, team_id, is_final):<br>
Check if a review has been submitted using the given reviewer, reviewee, team_id, and is_final
INPUT: -self,
        -reviews_table (an instance of gbmodel.reports() class that we use to make our database call),
        -reviewer_id (the id of the student who authored the review we are looking for),
        -reviewee_id (the id of the student being reviewed),
        -team_id (the id of the team the reviewer and reviewee are on),
        -is_final (a boolean to indicate if we are looking for a midterm or final review)
OUTPUT: a boolean indiating if the review was found in the database or not

display_error(self, error):<br>
Prints a given error message to the console and returns a rendering (?) of the viewStudent template
with a generic error message in it
INPUT: -self,
        -error (the error we wil to print to the console)
OUTPUT: an error page rendering of the viewStudent template 

post(self):<br>
A function that determines how the viewStudent class handles POST requests
INPUT: self
OUTPUT: a rendering of the viewStudent.html file. The information included in the rendering depends on
        the information we get from the POST request

## gbmodel/model_sqlalchemy.py

handle_exception():<br>
A global method which provides error handling in the event of a database error.
It rollsback the current database session and writes out logging information on the error.

##### professors
A model class which keeps track of capstone professors -- reflects the professors table in the database with its attributes.

get_professor(self, id):<br>
Get a professor with the given id
Input: professor id
Output: the professor object associated with the given id

get_all_professors(self):<br>
Get a list of all professors in the database (by id)
Input: none
Output: a list of professors

check_professor(self, prof_id):<br>
Checks if professor ID exists in the DB
Input: professor ID given
Output: True if it exists, False otherwise

prof_id(self, name):<br>
Gets the id of the professor with the given name, if he is found. Returns -1 otherwise
Input: professor name
Output: return professor's id

##### teams
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

get_max_team(self):<br>
Calculate the next id for a newly added team
if the table is empty, returns 1
Otherwise, return the max id+1

check_dup_team(self, t_name, session_id):<br>
Check if the new team name already existed in the given session
Input: name of the new team and session id of the selected session
Output: return False if the team already exists, True otherwise

insert_team(self, session_id, t_name):<br>
Insert a team to database
Input: self, session id and name of the new team

get_team_session_id(self, session_id):<br>
Get a list of all of the teams in a session
Input: session id of the selected session
Output: list of teams and their info from the selected session

remove_team_from_session(self, name, session_id):<br>
Remove a team and all the students from that team
Input: name of the team and session id
Output: True if the operation completed successfully. False if something went wrong

remove_team(self, name, session_id):<br>
Remove a team and all the students from that team
Input: name of the team and session id
Output: delete a team
        move all student in the team to unassigned student

dashboard(self, session_id):<br>
Return a lists of sessions from the database
and a list of teams + students from a selected session
Input: session id of the selected session

get_team_from_id(self, team_id):<br>
Get the team object associated with the given id
Input: team_id
Output: a team object, if found. None otherwise

##### students
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

get_team_members(self, tid):<br>
Get all members of a team
Input: team id as tid
Output: A list of student objects representing the students on that team

check_dup_student(self, id, session_id):<br>
        Check if a student already exits in a session
        Input: id of the student and selected session id
        Output: return False if the student was already in
                return True otherwise
                
insert_student(self, name, email_address, id, session_id, t_name):<br>
        Add new student
        Input: student name, student email address, student id, team name and id of the selected session
        Output: return False if student id already exists in the current session
                add student to the database and return True otherwise

get_user_sessions(self, student_id):<br>
        Returns all capstone sessions that a user belongs to
        Input: student_id: The database id of the student to retrieve capstone session ids for
        output: an array of objects representing the rows for each capstone the student belongs to

get_student_in_session(self, sid, session_id):<br>
        Get a student from the students table
        Input: student id, session id
        Output: the student that we found, or none if nothing was found

remove_student(self, sts, t_name, session_id):<br>
        Remove a list of selected students
        Input: list of students, team name and session id
        Output: return False of the list of student is empty or if something went wrong
            otherwise, remove student from the team

validate(self, id):<br>
        validate cas username with student id in the database
        Input: student id
        Output: object of found student

get_unassigned_students(self, s_id):<br>
        Get students from a session that do not have a team.
        Input: session id to grab students
        Output: Students who have no team.

edit_student(self, id, new_name, new_email):<br>
        Allows students to edit their name and email address
        Input: student's new email and name and current user id
        Output: apply new name and email to students in student table

set_lead(self, session_id, team_name, lead):<br>
Professor can set a lead for each team
Input: self, chosen session id, team name and lead name
Output: set True to team lead and False to the rest of students in the team

get_student_in_session(self, sid, session_id):<br>
Get a student from the students table
Input: student id, session id
Output: the student that we found, or none if nothing was found

check_team_lead(self, s_id, sess_id):<br>
Check if the student passed in by id is the team lead
Input: student id of the student to check
Output: True if the student is a team lead, False otherwise

set_active(self, session_id, option):<br>
Sets the active attribute in student
For a student to be able to access their reviews, "open" must be set
Inputs: The capstone session id of the class to set as active or not. Option as 'open' or 'close'.
"Open" to allow students to submit/edit reviews, "close" to not allow review submission.
Outputs: True to indicate success, False to indicate an error.

##### capstone_session
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

check_review_state(self, session_id, date):<br>
Given a capstone session id to check and a date,
this method determines the currently available review if any
Inputs: a capstone session id and a date which should be a python date time object
Outputs: 'final' if date is after the final start date for the session
'midterm' if the date is between the midterm and final start dates.
'error' otherwise

check_not_late(Self, session_id, date, type):<br>
This method is for determining is a review is late. It receives the type of review to check
and compares the date sent into the method with the review's end period
Inputs: session_id -- the value of the id for the capstone session to check
date: the date that the review is submitted, type: "midterm" or "final" should be received
Outputs: True -- the review is within the open period (the review is NOT late)
or False -- the review IS late or an error was experienced

get_sess_by_id(self, id):<br>
Get the capstone session object associated with the given id
inputs: id of capstone session to retrieve
outputs: capstone session object if found, none otherwise

check_term_name(self, s_term):<br>
Checks if the name of the term is valid
Input: start term of new session
Output: return True if valid, False otherwise

check_dup_session(self, s_term, s_year, p_id):<br>
Check if the new session name already exists in the database
Input: start term & year of the new session
Output: return False if the team already exists, True otherwise

get_active_sessions(self):<br>
Get a list of active capstone sessions
Input: self
Output: the list of currently active capstone sessions

check_dates(self, start, end):<br>
Check if start and end dates are valid
Input: start and end dates
Output: Return 0 if valid (both start and end date being empty is valid)
        Return 1 if start date is after the end date
        Return 2 if either start date or end date is empty (but not both)

check_not_late(Self, session_id, date, type):<br>

This method is for determining is a review is late. It receives the type of review to check
and compares the date sent into the method with the review's end period
Inputs: session_id -- the value of the id for the capstone session to check
date: the date that the review is submitted, type: "midterm" or "final" should be received
Outputs: True -- the review is within the open period (the review is NOT late)
or False -- the review IS late or an error was experienced


##### reports
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

get_reports_for_student(self, student_id, session_id, is_final=None):<br>
Gets all available reports for a student, optionally filtering to only midterms or finals
Input: student id, session_id and is_final (is_final indicates if we are filtering for final reviews
or not. is_final = true indicates we are looking for final reviews. is_final = false indicates
we are looking for midterm reviews. is_final = None indicates we want both.
Output: the available reports for the student

get_report(self, reviewer_id, reviewee_id, team_id, is_final):<br>
Get a review from the database using the given information
Input: reviewer_id (a student id), reviewee_id (a student id), team_id, is_final (indicates if the
review is a final review or not)
Output: the review, if it was found, or None if it wasn't or if there was a problem

get_team_reports(self, tid, is_final):<br>
This method is for getting the reports of an entire team
Inputs: tid -- team id of reports to retrieve, is_final - if it's the second term
Outputs: result - all report objects for the team

insert_report(self, sess_id, time, reviewer, tid, reviewee, tech,
                      ethic, com, coop, init, focus, cont, lead, org, dlg,
                      points, strn, wkn, traits, learned, proud, is_final, late):<br>
Stages a report to be inserted into the database -- This does NOT commit the add!
Inputs: Arguments for each individual field of the report
Outputs: true if adding was successful, false if not

commit_reports(self, id, state, sess_id, success):<br>
Method to commit changes to the DB through the model while updating the user's state
input: None
output: True if successful, false otherwise

commit_updates(self, success):<br>
This method is for committing review updates following several being edited.
It should be called whenever reports are edited, but not added.
input: success -- a boolean object indicating whether to proceed
with committing (true) or to roll back (false)
output: False -- commit was not made, True - commit was made successfully

##### removed_students
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

add_student(self, s):<br>
Insert removed students into remocved_students table
Input: student info
Output: return False if the info is empty
Otherwise, add student to the list and return True
