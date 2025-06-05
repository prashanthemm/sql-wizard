# import argparse
# from converters.pg_to_oracle import convert_file

import argparse
# from converters.pg_to_oracle import convert_file
from parser import convert_pg_to_oracle
import os
import logging

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# logging configuration
logger = logging.getLogger('app.log')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(log_dir, 'app.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

#loggin name changed

def translate_and_save(file_path:str):
    """Translates the data  and saves it"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            pg_content = f.read()
        logger.debug('Data retrieved from %s', file_path)
        pg_procedures = [proc.strip() for proc in pg_content.split("\n\n\n\n\n") if proc.strip()]
        oracle_procedures = []
        for i, pg_proc in enumerate(pg_procedures, 1):
            try:
                oracle_proc = convert_pg_to_oracle(pg_proc)
                oracle_procedures.append(oracle_proc.strip())
            except Exception as e:
                logger.error('Error converting procedure number %d : %s', i, e)

        out_path = r"c:\Users\PrashantKumar\Desktop\sql-wizard\output\processed_data.sql"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n\n\n".join(oracle_procedures))  # Oracle-style separator

        logger.debug('Converted %d procedure(s) saved to %s', len(oracle_procedures), out_path)

    except Exception as e:
        logger.error('Failed to translate and save: %s', e)


def main():
    try:
        translate_and_save("input_extraction/raw_data.sql")  # TBD include import path from dvc.yaml
    except Exception as e:
        logger.error('Translate didn\'t even started: %s', e)
        raise


if __name__ == "__main__":
    main()

