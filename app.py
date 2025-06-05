import openai
import time
import os
import logging

# Set your OpenAI API Key
openai.api_key = os.getenv("api")  # or directly assign your key here

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("conversion.log", mode='w')
    ]
)

# PostgreSQL queries to convert
pg_queries = [
    "CREATE FUNCTION add_numbers(a INT, b INT) RETURNS INT AS $$ BEGIN RETURN a + b; END; $$ LANGUAGE plpgsql;",
    "CREATE PROCEDURE greet_user(name TEXT) LANGUAGE plpgsql AS $$ BEGIN RAISE NOTICE 'Hello, %', name; END; $$;",
    "INSERT INTO employees (id, name) VALUES (1, 'John Doe');",
    "CREATE TABLE departments (id INT PRIMARY KEY, dept_name TEXT);"
]

def batch_convert_pg_to_oracle(queries, batch_size=3, delay=2):
    converted_results = []

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]

        # Construct the prompt
        prompt = "Convert the following PostgreSQL SQL statements into Oracle SQL syntax. Clearly number the conversions.\n\n"
        prompt += "PostgreSQL Queries:\n"
        for idx, query in enumerate(batch, start=1):
            prompt += f"{idx}. {query}\n"

        prompt += "\nOracle SQL:\n"

        try:
            logging.debug(f"Sending batch {i // batch_size + 1} to ChatGPT...")

            response = openai.ChatCompletion.create(
                model="gpt-4o",  # or "gpt-4o-mini" if you've exhausted GPT-4o free tier
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            result_text = response.choices[0].message.content.strip()
            converted_results.append(result_text)

            logging.debug(f"Batch {i // batch_size + 1} conversion successful.")
            time.sleep(delay)  # delay to stay within rate limits

        except Exception as e:
            logging.error(f"Batch {i // batch_size + 1} conversion failed: {e}")
            converted_results.append(f"-- Error in batch {i // batch_size + 1} --")

    return converted_results

if __name__ == "__main__":
    logging.info("Starting PostgreSQL to Oracle SQL conversion using ChatGPT API...")

    results = batch_convert_pg_to_oracle(pg_queries, batch_size=2)

    output_file = "converted_oracle.sql"
    with open(output_file, "w") as f:
        for batch in results:
            f.write(batch + "\n\n")

    logging.info(f"Conversion completed. Output written to {output_file}")
