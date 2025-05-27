import psycopg2
import os

def export_procedures(output_file):
    conn = psycopg2.connect(
        dbname="postgres",      # Replace with your DB name
        user="postgres",        # Replace with your username
        password="1234",  # Replace securely or use environment variables
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT
            pg_get_functiondef(p.oid) AS definition
        FROM
            pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE
            p.prokind = 'p'
            AND n.nspname = 'public';
    """)
    results = cur.fetchall()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        for row in results:
            f.write(row[0] + '\n\n\n\n')

    cur.close()
    conn.close()
    print(f"Exported {len(results)} procedures to {output_file}")

# Run it
if __name__ == "__main__":
    export_procedures("examples/fin_test1.sql")
