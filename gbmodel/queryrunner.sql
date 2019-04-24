-- SQLite

select * from capstone_session;

select * from teams;

select * from students;

select * from removed_students;

select name from students where name = 'lvn2'

delete from students where name = 'lvn2'

INSERT INTO students (id, tid, session_id, name, is_lead, midterm_done, final_done, active)
VALUES (1111,222,0,'lvn2',0,0,0,'midterm')