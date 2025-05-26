



CREATE OR REPLACE PROCEDURE insert_test(
    p_id   NUMBER,
    p_name VARCHAR2
)
IS
BEGIN
    INSERT INTO test_proc (id, name) VALUES (p_id, p_name);
    COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE insert_test2(
    p_id   NUMBER,
    p_name VARCHAR2
)
IS
BEGIN
    INSERT INTO test_proc (id, name) VALUES (p_id, p_name);
    COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE insert_test3(
    p_id   NUMBER,
    p_name VARCHAR2
)
IS
BEGIN
    INSERT INTO test_proc (id, name) VALUES (p_id, p_name);
    COMMIT;
END;

/



