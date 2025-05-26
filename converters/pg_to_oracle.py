import json
import re

# Load type mappings
with open("rules/type_mappings.json") as f:
    PG_TO_ORACLE = json.load(f)

def convert_line(line):
    for pg_term, oracle_term in PG_TO_ORACLE.items():
        # Replace whole words only (case-insensitive)
        line = re.sub(rf'\b{re.escape(pg_term)}\b', oracle_term, line, flags=re.IGNORECASE)
    return line

def convert_file(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            converted = convert_line(line)
            outfile.write(converted)
