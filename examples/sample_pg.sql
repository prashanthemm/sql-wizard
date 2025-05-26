CREATE PROCEDURE insert_test(IN numeric, IN character varying)
LANGUAGE plpgsql
AS $procedure$
BEGIN
    INSERT INTO test_proc (id, name) VALUES ($1, $2);
    COMMIT;
END;
$procedure$;
