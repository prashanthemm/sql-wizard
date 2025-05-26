CREATE TABLE users (
    id SERIAL,
    active BOOLEAN,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

SELECT * FROM users WHERE description ILIKE '%admin%';
