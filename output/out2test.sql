CREATE OR REPLACE PROCEDURE public.insert_test(param1 IN NUMBER, param2 IN VARCHAR2) IS
BEGIN
insert into public.test_proc (id, name) values (param1,param2);
commit;

END;
/


CREATE OR REPLACE PROCEDURE public.insert_test2(param1 IN NUMBER, param2 IN VARCHAR2) IS
BEGIN
insert into public.test_proc (id, name) values (param1,param2);
commit;

END;
/


CREATE OR REPLACE PROCEDURE public.insert_test3(param1 IN NUMBER, param2 IN VARCHAR2) IS
BEGIN
insert into public.test_proc (id, name) values (param1,param2);
commit;

END;
/