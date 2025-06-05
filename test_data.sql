CREATE PROCEDURE sp_hello_world()
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Hello, World!';
END;
$$;





CREATE PROCEDURE sp_greet_user(IN username TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Hello, %', username;
END;
$$;





CREATE PROCEDURE sp_add_numbers(IN a INT, IN b INT, OUT sum INT)
LANGUAGE plpgsql
AS $$
BEGIN
    sum := a + b;
END;
$$;





CREATE PROCEDURE sp_double_value(INOUT val INT)
LANGUAGE plpgsql
AS $$
BEGIN
    val := val * 2;
END;
$$;





CREATE PROCEDURE sp_check_even_odd(IN num INT)
LANGUAGE plpgsql
AS $$
DECLARE
    result TEXT;
BEGIN
    IF num % 2 = 0 THEN
        result := 'Even';
    ELSE
        result := 'Odd';
    END IF;
    RAISE NOTICE 'The number is %', result;
END;
$$;





CREATE PROCEDURE sp_print_loop(IN max_count INT)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
BEGIN
    WHILE i <= max_count LOOP
        RAISE NOTICE 'Count: %', i;
        i := i + 1;
    END LOOP;
END;
$$;





CREATE PROCEDURE sp_print_employees()
LANGUAGE plpgsql
AS $$
DECLARE
    emp RECORD;
    emp_cursor CURSOR FOR SELECT name FROM employees;
BEGIN
    OPEN emp_cursor;
    LOOP
        FETCH emp_cursor INTO emp;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Employee: %', emp.name;
    END LOOP;
    CLOSE emp_cursor;
END;
$$;





CREATE PROCEDURE sp_divide(IN a INT, IN b INT, OUT result FLOAT)
LANGUAGE plpgsql
AS $$
BEGIN
    BEGIN
        result := a / b;
    EXCEPTION
        WHEN division_by_zero THEN
            RAISE NOTICE 'Division by zero!';
            result := NULL;
    END;
END;
$$;





CREATE PROCEDURE sp_insert_employee(IN name TEXT, IN salary NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO employees(name, salary) VALUES (name, salary);
END;
$$;





CREATE PROCEDURE sp_wrapper()
LANGUAGE plpgsql
AS $$
BEGIN
    CALL sp_hello_world();
END;
$$;





CREATE PROCEDURE sp_temp_table()
LANGUAGE plpgsql
AS $$
BEGIN
    CREATE TEMP TABLE temp_numbers (num INT);
    INSERT INTO temp_numbers VALUES (1), (2), (3);
    RAISE NOTICE 'Temporary table created and populated';
END;
$$;





CREATE PROCEDURE sp_dynamic_insert(IN tablename TEXT, IN val TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('INSERT INTO %I (data) VALUES (%L)', tablename, val);
END;
$$;
