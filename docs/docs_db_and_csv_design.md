
## Capstone 360 Developer Documentation -- Database and CSV Design

The purpose of this document is to provide an overview of the the application's expected database schema and CSV formatting for student information ppload


### Database Schema

#### capstone_session
|--------------------------------------------------------------------------------|
| Attribute Name   | Type         | Can Be Null | Default Value | Foreign Key To |
|------------------|--------------|-------------|---------------|----------------|
| id               | INTEGER      | No          | -             | -              |
| start_term       | VARCHAR(10)  | No          | -             | -              |
| start_year       | INTEGER      | No          | -             | -              |
| end_term         | VARCHAR(10)  | No          | -             | -              |
| end_year         | INTEGER      | No          | -             | -              |
| midterm_start    | TIMESTAMP    | Yes         | -             | -              |
| midterm_end      | TIMESTAMP    | Yes         | -             | -              |
| final_start      | TIMESTAMP    | Yes         | -             | -              |
| final_end        | TIMESTAMP    | Yes         | -             | -              |
| professor_id     | VARCHAR(128) | No          | -             | professors(id) |

#### students table
| Attribute Name | Type         | Can Be Null | Default Value | Foreign Key To       |
|----------------|--------------|-------------|---------------|----------------------|
| id             | VARCHAR(128) | No          | -             | -                    |
| tid            | INTEGER      | No          | -             | team(id)             |
| session_id     | INTEGER      | No          | -             | capstone_session(id) |
| name           | VARCHAR(128) | No          | -             | -                    |
| is_lead        | BOOLEAN      | No          | FALSE         | -                    |
| midterm_done   | BOOLEAN      | No          | FALSE         | -                    |
| final_done     | BOOLEAN      | No          | FALSE         | -                    |
| active         | VARCHAR(128) | Yes         | -             | -                    |
| email_address  | VARCHAR(128) | No          | -             | -                    |

#### teams table
| Attribute Name | Type         | Can Be Null | Default Value | Foreign Key To |
|----------------|--------------|-------------|---------------|----------------|
| id             | INTEGER      | No          | -             | -              |
| session_id     | INTEGER      | No          | -             | session(id)    |
| name           | VARCHAR(128) | No          | -             | -              |

#### removed_students
| Attribute Name   | Type         | Can Be Null | Default Value | Foreign Key To           |
|------------------|--------------|-------------|---------------|--------------------------|
| id               | VARCHAR(128) | No          | -             | -                        |
| tid              | INTEGER      | No          | -             | teams(id) (unenforced)   |
| session_id       | INTEGER      | No          | -             | session(id) (unenforced) |
| name             | VARCHAR(128) | No          | -             | -                        |
| is_lead          | BOOLEAN      | No          | FALSE         | -                        |
| midterm_done     | BOOLEAN      | No          | FALSE         | -                        |
| final_done       | BOOLEAN      | No          | FALSE         | -                        |
| removed_date     | TIMESTAMP    | No          | -             | -                        |

#### professors
| Attribute Name | Type         | Can Be Null | Default Value | Foreign Key To |
|----------------|--------------|-------------|---------------|----------------|
| id             | VARCHAR(128) | No          | -             | -              |
| name           | VARCHAR(128) | No          | -             | -              |

#### reports
|-------------------------|---------------|---------------|---------------|---------------------------|
| Attribute Name          | Type          | Can Be Null   | Default Value | Foreign Key To            |
|-------------------------|---------------|---------------|---------------|---------------------------|
| time                    | TIMESTAMP     | No            | -             | -                         |
| session_id              | INTEGER       | No            | -             | -                         |
| reviewer (sid)          | VARCHAR(128)  | No            | -             | students(id) (unenforced) |
| tid (tid)               | INTEGER       | No            | -             | teams(id)                 |
| reviewee (sid)          | VARCHAR(128)  | No            | -             | students(id) (unenforced) |
| tech_mastery            | INTEGER       | Yes           | -             | -                         |
| work_ethic              | INTEGER       | Yes           | -             | -                         |
| communication           | INTEGER       | Yes           | -             | -                         |
| cooperation             | INTEGER       | Yes           | -             | -                         |
| initiative              | INTEGER       | Yes           | -             | -                         |
| team_focus              | INTEGER       | Yes           | -             | -                         |
| contribution            | INTEGER       | Yes           | -             | -                         |
| leadership              | INTEGER       | Yes           | -             | -                         |
| organization            | INTEGER       | Yes           | -             | -                         |
| delegation              | INTEGER       | Yes           | -             | -                         |
| points                  | INTEGER       | No            | -             | -                         |
| strengths               | VARCHAR(4096) | Yes           | -             | -                         |
| weaknesses              | VARCHAR(4096) | Yes           | -             | -                         |
| traits_to_work_on       | VARCHAR(4096) | Yes           | -             | -                         |
| what_you_learned        | VARCHAR(4096) | Yes           | -             | -                         |
| proud_of_accomplishment | VARCHAR(4096) | Yes           | -             | -                         |
| is_final                | BOOLEAN       | No            | -             | -                         |
| is_late                 | BOOLEAN       | Yes (for now) | -             | -                         |

### CSV Formatting
When importing students via .csv, each row in the .csv should be formatted in the following manner;
firstName lastName, studentID, teamName
This will the create a student with the given name and assign them to the named team.

