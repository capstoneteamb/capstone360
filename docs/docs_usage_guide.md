
## Capstone 360 Developer Documentation -- Usage Guide

The purpose of this document is to provide an overview of the application's functionality from a professor and student persepective

Professors and Students will need to sign in through the CAT's CAS log in system with an MCECS username.
Professors and students access their workflows via the approriate log in button.

### Professors

#### Selecting a capstone session

1. In the top left of the page, there is a drop down menu. 
2. Select the session you which you access

#### Adding capstone sessions

1. Click 'Edit'
2. Click 'Add Session'
3. For Term, enter 'Fall,' 'Winter,' 'Spring,' or 'Summer' to indicate the starting term of the session
4. For year, enter the year that corresponds to the starting term in 4 digit form (ex: 2020)
5. From the dropdown menu, choose a professor to be assigned to oversee the term.
6. Click 'Add Session'
7. A new session will be created with no students or teams.

#### Removing Capstone Sessions

1. Click 'Edit'
2. Click 'Remove Session'
3. 'Delete Session' **WARNING: This will remove all information related to that session**

#### Adding Student

Add in bulk via CSV:
1. Click 'Edit'
2. Click 'Import Students'
3. Click 'Browse'
4. Choose csv file to upload
5. Click import
7. Teams and Students will be automatically created and displayed on the professor dashboard

Student self-regitration:<br>
Students may sign themselves up for an ongoing capstone course. They will be placed into the capstone session without a team.
To assign students to a team:

1. Click 'Edit'
2. Click 'Assign Team'
3. For each student, enter the name of the team they will be placed on
4. If a team name is entered which does not already exist, a team will be created for that student.
5. If this was done on accident, delete the erroneous team and re-assign the student.

Manual Adding:
If a single student needs to be placed on a team:
1. Click 'Edit'
2. Scroll to the desired team
3. Click 'Add Student'
4. Enter the student name
5. Enter the student's database ID (this may need to be retrieved from the student)
6. Enter the student's email address (this may be left blank)
7. click 'Add Student'

#### Removing Students

To remove a student from a team (removes them from the capstone session as well):
1. Click 'Edit'
2. Click 'Remove'
3. Click the checkbox next to a student on the team you wish to remove them from
4. Click 'Remove Student'

#### Adding Teams

Note: adding students by CSV automatically creates teams

1. Click 'Edit'
2. Click 'Add Team'
3. Enter the team name
4. Click 'Add Team'

#### Removing Teams

Note: Removing a team unassigns the student from that team and places them on an unassigned list.
**Removing a team will remove reviews submitted for that team**

1. Click 'Edit'
2. Click 'Remove'
3. Scroll to the team you wish to remove
4. Click 'Remove Team'

#### Setting Team Leads

1. Click 'Edit'
2. click 'Set Lead'
3. For each team:
4. Click the checkbox next to the student you wish to assign as team lead
5. Click 'Submit'

#### Review Access Control and Late Reviews

Granting access to reviews is done in two ways.
Reviews must first be assigned 'dates' which function by the following logic:

If a "final" review start date is set:
Students can access final reviews on or after that date

If a "midterm" review start date is set:
Students can access midterm reviews on or after that date up until the date that final dates start.

If a review is submitted after a "final" review end date is set:
The final review will be marked as late

If a midterm review is submitted after a "midterm" review end date is set:
The midterm review will be marked as late.

To set review dates:

1. Click 'Edit'
2. Click 'Set Review Dates'
3. Use the calendar tool to set dates for the midterm and or the final reviews.
4. Be sure to set a start and end date
5. Click 'Submit'

If you wish to close off reviews (for example, to prevent students from editing reviews after reports have been generated),
you may set reviews to be "Open" (available) or "Closed" (unavailable to be filled out or edited).

To Open/Close Reviews:

1. Click 'Edit'
2. Click 'Open/Close Reviews'
3. Use the drop down to select open or closed
4. Click 'Submit'

**Remember to re-open reviews on the final start date if you close them for the midterm**

#### Anonymous Report Generation

To generate anonymous reports for student distribution:

1. In the top left, click the drop down menu for 'Generate Reports'
2. Click 'Midterm' or 'Final' for midterm reports or final reports
3. You'll be taken to a web page containing all reports.
4. Print the page -- reports will automatically be divided to be printed on individual pages

#### Report Analysis

Dashboard Analysis:
If 'midterm' or 'final' review dates have been set, and it is currently after one of those dates,
point ranges will be displayed next to each student if reviews have been filled out for that student.

Individual report analysis:
1. Click on a student name
2. You'll be taken to a 'viewStudent' page containing a list of team members and a 'Report' button
3. For all team members the student has submitted reports for, you may click on the students name to see the report the student has filled out for that team member
4. If no review is present, a message saying so will be displayed

To see the student's de-anonymized report:
1. From the 'viewStudent' page described above, click 'Report'

### Students



