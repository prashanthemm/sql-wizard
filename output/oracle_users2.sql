CREATE OR REPLACE PROCEDURE public.insert_test(IN numeric, IN character varying)
 LANGUAGE plpgsql
AS $procedure$

begin
insert into public.test_proc (id, name) values ($1,$2);
commit;

end;
$procedure$


