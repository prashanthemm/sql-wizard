import psycopg2
import os
import logging
import yaml
from dotenv import load_dotenv
from pathlib import Path

# Ensure the "logs" directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)


# logging configuration
logger = logging.getLogger('input_extraction')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(log_dir, 'input_extraction.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def export_procedures(output_file: str):
    """Importing data from PostgreSQL database"""
    try:
        logger.debug('Connecting to the PostgreSQL database')
        env_path = Path(__file__).resolve().parents[1] / '.env'
        load_dotenv(dotenv_path=env_path)
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),      
            user=os.getenv("DB_USER"),       
            password=os.getenv("DB_PASSWORD"),      
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        logger.debug('Connected to PostgreSQL database')

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
                f.write(row[0] + '\n\n\n\n\n')

        cur.close()
        conn.close()
        logger.debug('Data imported to %s', output_file)

    except Exception as e:
        logger.error('Failed to  complete data ingestion process: %s', e)
        raise


def main():
    try:
        export_procedures("input_extraction/raw_data.sql")
    except Exception as e:
        logger.error('Failed to extract data from PostgreSQL database: %s', e)
        raise


# Run it
if __name__ == "__main__":
    main()
    # export_procedures("examples/raw.sql")
