# import argparse
# from converters.pg_to_oracle import convert_file

# def main():
#     parser = argparse.ArgumentParser(description="Convert PostgreSQL SQL to Oracle-compatible SQL.")
#     parser.add_argument("input", help="Path to the input PostgreSQL SQL file")
#     parser.add_argument("output", help="Path to save the converted Oracle SQL file")
#     args = parser.parse_args()

#     convert_file(args.input, args.output)
#     print(f"Conversion complete. Output saved to {args.output}")

# if __name__ == "__main__":
#     main()

# File: visitor.py (or another driver script inside sql-wizard)


import argparse
from converters.pg_to_oracle import convert_file

def main():
    parser = argparse.ArgumentParser(description="Convert PostgreSQL procedures to Oracle")
    parser.add_argument('input', help='Path to PostgreSQL SQL file')
    parser.add_argument('output', help='Path to write Oracle-compatible SQL')
    args = parser.parse_args()

    convert_file(args.input, args.output)



from visitor import convert_pg_to_oracle

if __name__ == "__main__":
    
    with open("examples/fin_test1.sql", "r", encoding="utf-8") as f:
        pg_content = f.read()

    
    pg_procedures = [proc.strip() for proc in pg_content.split("\n\n\n\n") if proc.strip()]

    
    oracle_procedures = []
    for i, pg_proc in enumerate(pg_procedures, 1):
        try:
            oracle_proc = convert_pg_to_oracle(pg_proc)
            oracle_procedures.append(oracle_proc.strip())
        except Exception as e:
            print(f"⚠️ Error converting procedure #{i}: {e}")

    out_path = r"c:\Users\PrashantKumar\Desktop\sql-wizard\output\out2test.sql"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n\n".join(oracle_procedures))  # Oracle-style separator

    print(f"✅ Converted {len(oracle_procedures)} procedure(s) written to 'out2test.sql'")




# from visitor import convert_pg_to_oracle  # If convert_pg_to_oracle is defined in visitor.py

# if __name__ == "__main__":
#     with open("examples/fin_test1.sql", "r", encoding="utf-8") as f:
#     pg_proc = f.read()


#     oracle_proc = convert_pg_to_oracle(pg_proc)


#     with open("converted_output.sql", "w", encoding="utf-8") as f:
#     f.write(oracle_proc)

#     print("✅ Oracle SQL procedure written to 'converted_output.sql'")
