# Classes Summary

## form. py
##### class review
The review class handles get and post requests for reivew.html, and it includes helper functions for cleanliness

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