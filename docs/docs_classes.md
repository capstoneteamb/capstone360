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

##### class AddStudent
This class handles get request for addStudent.html

##### class AddSession
This class handles get requests for addStudent.html

##### class RemoveSession
This class handles get requests for removeSession.html

##### class AddTeam
This class handles get requests for addTeam.html

##### class AddTeamCSV
This class handles import students via CSV file

##### class RemoveTeam
This class handles get requests for removeTeam.html

##### class SetDate
This class handles get requests for setDate.html

##### class AssignTeam
This class handles team assignment for assignTeam.html

## report. py

##### class MissingStudentException
Exception class to raise exception if no students for a given team or session are found

##### class MissingTeamException
Exception class to raise exception if no team is in the database when searched

##### class GeneratedProfessorReportView
Generates a report for a specific student, for viewing by a professor.

##### class GeneratedAnonymousReportView
Generates all anonymized reports for printing and handing out to students.

## student_dashboard.py

##### class StudentDashboard
Student Dashboard class handles get requests from index.html when student login button is clicked on.

##### class EditStudent
Edit Student class handles get requests from student Dashboard when Edit is clicked on

## student_register.py

##### class StudentRegister
Facilitates the rendering and processing of the register student page, which allows students to register for a currently ongoing capstone session

## view_register.py

##### class ViewReview
A method view class that oversees the viewing of individual student reviews

## view_student.py

##### class ViewStudent
A class for the student page (that a professor would access from the professor dashboard. The professor should be able to use this page to access the midterm and final reviews for a student.)

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

##### students
A model class which keeps track of capstone teams -- reflects the teams table in the database with its attributes.

get_team_members(self, tid):<br>
Get all members of a team
Input: team id as tid
Output: A list of student objects representing the students on that team

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
