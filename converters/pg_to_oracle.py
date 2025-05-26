import os
import json
import re

# Load type mappings
with open("rules/type_maps.json") as f:
    PG_TO_ORACLE = json.load(f)

def convert_line(line):
    for pg_term, oracle_term in PG_TO_ORACLE.items():
        line = re.sub(rf'\b{re.escape(pg_term)}\b', oracle_term, line, flags=re.IGNORECASE)
    return line

def convert_file(input_path, output_path):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            converted = convert_line(line)
            outfile.write(converted)
