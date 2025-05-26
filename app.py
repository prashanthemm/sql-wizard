import argparse
from converters.pg_to_oracle import convert_file

def main():
    parser = argparse.ArgumentParser(description="Convert PostgreSQL SQL to Oracle-compatible SQL.")
    parser.add_argument("input", help="Path to the input PostgreSQL SQL file")
    parser.add_argument("output", help="Path to save the converted Oracle SQL file")
    args = parser.parse_args()

    convert_file(args.input, args.output)
    print(f"Conversion complete. Output saved to {args.output}")

if __name__ == "__main__":
    main()
