
## Capstone 360 Developer Documentation -- Glossary

The purpose of this document is to provide meanings for commonly used terms in these guides, code comments, the code, and the application

Session -- 'Session' is a term which has a few uses and may refer to "capstone sessions," flask sessions, or model sqlalchemy sessions.
For flask sessions, see: https://pythonhosted.org/Flask-Session/ For model sqlalchemy sessions, see: https://docs.sqlalchemy.org/en/13/orm/session.html
For capstone sessions, see the entry below:

Capstone Session -- A capstone session refers to one instanstiation of a capstone course. 
A capstone session is associated with a start term and end term and a start year and end year. For example, Fall 2019-Winter2020.
It has a "capstone session ID," sometimes referred to as a session ID which is an internal identifier for a database record
containing the information of a capstone session.

ID -- This is a term used to refer to an internal database identifier , and may or may not correspond to a counterpart outside
of the application and database context. For instance, a "student ID" is not actually the PSU student ID for a student record.
For more information on which tables an ID pertains to, see the database schema.

Professor -- A current capstone course instructor, or someone who has been granted access to the administrative side of the application.

Student -- A capstone course student who may access the student side of the application.

Review -- A form that a student fills out to contribute to a report for their team.

Report -- A compliation of submitted review data for analysis.

Professor Dashboard -- The main page from which a professor administers capstone sessions, students, reviews, and reports.

Student Dashboard -- A log in page from which students may access reviews or an edit menu
