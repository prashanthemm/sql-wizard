import os
import json
import re
##useless so far
# # Load type mappings
# with open("rules/type_maps.json") as f:
#     PG_TO_ORACLE = json.load(f)

# def convert_line(line):
#     for pg_term, oracle_term in PG_TO_ORACLE.items():
#         line = re.sub(rf'\b{re.escape(pg_term)}\b', oracle_term, line, flags=re.IGNORECASE)
#     return line

# def convert_file(input_path, output_path):
#     # Ensure output directory exists
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
#         for line in infile:
#             converted = convert_line(line)
#             outfile.write(converted)


import re
# -------------------------------------------------------------------
# def convert_procedure_block(pg_code: str) -> str:
#     # Extract procedure name and parameters
#     match = re.search(r"CREATE\s+PROCEDURE\s+(\w+)\s*\((.*?)\)", pg_code, re.IGNORECASE | re.DOTALL)
#     if not match:
#         return "-- [ERROR] Couldn't parse procedure header\n" + pg_code

#     proc_name = match.group(1)
#     param_block = match.group(2).strip()

#     # Convert parameters
#     params = []
#     for p in param_block.split(','):
#         p = p.strip()
#         if not p:
#             continue
#         parts = p.split()
#         if len(parts) >= 2:
#             param_name = "p_" + str(len(params) + 1)
#             datatype = parts[1].upper().replace("CHARACTER VARYING", "VARCHAR2").replace("NUMERIC", "NUMBER")
#             params.append(f"{param_name} {datatype}")
    
#     param_str = ", ".join(params)

#     # Convert body (simple $1 -> p_1 etc.)
#     body = pg_code.split("AS", 1)[-1]
#     body = re.sub(r"\$([0-9]+)", lambda m: f"p_{m.group(1)}", body)
#     body = re.sub(r"LANGUAGE\s+plpgsql", "", body, flags=re.IGNORECASE)
#     body = re.sub(r"AS\s+\$.*?\$", "", body, flags=re.IGNORECASE)
#     body = re.sub(r"\$.*?\$", "", body, flags=re.IGNORECASE)
#     body = body.strip()

#     return f"""CREATE OR REPLACE PROCEDURE {proc_name}(
#     {param_str}
# )
# IS
# {body}
# /
# """

# def convert_file(input_path, output_path):
#     with open(input_path, 'r') as infile:
#         content = infile.read()

#     # DEBUG: print file content
#     print("\n--- Input File Content ---")
#     print(content[:300] + "\n...")  # Print first 300 characters to check structure

#     # More flexible regex to catch PL/pgSQL procedures
#     procedure_blocks = re.findall(
#         r"(CREATE\s+PROCEDURE\s+.*?LANGUAGE\s+plpgsql\s*;)", content,
#         re.IGNORECASE | re.DOTALL
#     )

#     print(f"\n[DEBUG] Found {len(procedure_blocks)} procedures.\n")

#     if not procedure_blocks:
#         print("[WARNING] No procedures matched. Please check your input formatting.")
#         return

#     converted_blocks = [convert_procedure_block(block) for block in procedure_blocks]

#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, 'w') as outfile:
#         outfile.write("\n\n".join(converted_blocks))

