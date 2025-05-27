from antlr4 import *
from antlr.PostgreSQLLexer import PostgreSQLLexer
from antlr.PostgreSQLParser import PostgreSQLParser
from antlr.PostgreSQLParserVisitor import PostgreSQLParserVisitor

# Map PostgreSQL types to Oracle types (expand as needed)
PG_TO_ORACLE_TYPES = {
    "integer": "NUMBER",
    "int": "NUMBER",
    "bigint": "NUMBER",
    "smallint": "NUMBER",
    "serial": "NUMBER",
    "bigserial": "NUMBER",
    "numeric": "NUMBER",
    "real": "FLOAT",
    "double precision": "FLOAT",
    "character varying": "VARCHAR2",
    "varchar": "VARCHAR2",
    "character": "CHAR",
    "char": "CHAR",
    "text": "CLOB",
    "boolean": "BOOLEAN",
    "date": "DATE",
    "timestamp": "TIMESTAMP",
    "time": "DATE",  # Oracle doesn't have TIME-only
}


# class PgToOracleVisitor(PostgreSQLParserVisitor):
#     def __init__(self):
#         super().__init__()
#         self.proc_name = ""
#         self.params = []
#         self.body = ""

#     def visitCreatefunctionstmt(self, ctx:PostgreSQLParser.CreatefunctionstmtContext):
#         # Extract procedure name
#         func_name_ctx = ctx.func_name()
#         # Usually func_name -> type_function_name -> identifier
#         self.proc_name = func_name_ctx.getText()  # You can customize deeper extraction if needed

#         # Extract parameters
#         if ctx.func_args_with_defaults():
#             params_ctx = ctx.func_args_with_defaults().func_args_with_defaults_list()
#             if params_ctx:
#                 self.visitFunc_args_with_defaults_list(params_ctx)

#         # Extract procedure body (func_as)
#         if ctx.createfunc_opt_list():
#             for opt in ctx.createfunc_opt_list().createfunc_opt_item():
#                 if opt.LANGUAGE():
#                     # Just detect LANGUAGE option, skip here
#                     continue
#                 if opt.AS():
#                     # opt.func_as() has the body
#                     self.visitFunc_as(opt.func_as())

#         return self  # or whatever you want

#     def visitFunc_args_with_defaults_list(self, ctx:PostgreSQLParser.Func_args_with_defaults_listContext):
#         params = []
#         for param_ctx in ctx.func_arg_with_default():
#             func_arg = param_ctx.func_arg()
#             # Extract mode (IN, OUT, etc.)
#             mode = func_arg.arg_class().getText() if func_arg.arg_class() else "IN"

#             # Extract parameter name (optional)
#             param_name = None
#             if func_arg.param_name():
#                 param_name = func_arg.param_name().getText()

#             # Extract type name (go deeper)
#             type_name = ""
#             if func_arg.func_type():
#                 type_name = func_arg.func_type().typename().getText()

#             params.append({"mode": mode, "name": param_name, "type": type_name})
#         self.params = params
#         return params

#     def visitFunc_as(self, ctx:PostgreSQLParser.Func_asContext):
#         # Extract raw body text (it includes $procedure$ delimiters)
#         body_text = ctx.sconst(0).getText()
#         # Remove $procedure$ delimiters if present
#         if body_text.startswith("$procedure$") and body_text.endswith("$procedure$"):
#             body_text = body_text[len("$procedure$"):-len("$procedure$")].strip()
#         self.body = body_text
#         return self.body

#     def format_params(self):
#         formatted_params = []
#         for p in self.params:
#             name = p['name'] if p['name'] else "param"
#             oracle_type = PG_TO_ORACLE_TYPES.get(p['type'].lower(), "VARCHAR2")
#             mode = p['mode'].upper()
#             formatted_params.append(f"{name} {mode} {oracle_type}")
#         return ", ".join(formatted_params)

#     def to_oracle_procedure(self):
#         header = f"CREATE OR REPLACE PROCEDURE {self.proc_name} ({self.format_params()}) IS\nBEGIN\n"
#         body = self.body + "\nEND;\n/"
#         return header + body


# def parse_and_convert_pg_proc(input_sql_text):
#     input_stream = InputStream(input_sql_text)
#     lexer = PostgreSQLLexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = PostgreSQLParser(stream)
#     tree = parser.stmt()  # parse the SQL as a statement

#     visitor = PgToOracleVisitor()
#     visitor.visit(tree)
#     return visitor.to_oracle_procedure()


# if __name__ == "__main__":
#     sample_pg_proc = """
#     CREATE PROCEDURE insert_test(IN numeric, IN character varying)
#     LANGUAGE plpgsql
#     AS $procedure$
#     BEGIN
#         INSERT INTO test_proc (id, name) VALUES ($1, $2);
#         COMMIT;
#     END;
#     $procedure$;
#     """

#     oracle_proc = parse_and_convert_pg_proc(sample_pg_proc)
#     print("Converted Oracle Procedure:\n")
#     print(oracle_proc)

#--------------------------------------------------------------------------------

class PgToOracleVisitor(PostgreSQLParserVisitor):
    def __init__(self):
        super().__init__()
        self.param_names = []
        self.param_types = []
        self.proc_name = ""
    
    def visitCreatefunctionstmt(self, ctx):
        # Extract procedure name
        self.proc_name = ctx.func_name().getText()
        
        # Extract parameters list
        params_ctx = ctx.func_args_with_defaults()
        self.param_names = []
        self.param_types = []
        if params_ctx:
            params_list = params_ctx.func_args_with_defaults_list()
            if params_list:
                for i, param_ctx in enumerate(params_list.func_arg_with_default()):
                    # Assign param names param1, param2, ...
                    param_name = f"param{i+1}"
                    self.param_names.append(param_name)

                    # Extract PostgreSQL type string
                    typ_ctx = param_ctx.func_arg().func_type().typename()
                    pg_type = typ_ctx.getText().lower()

                    # Convert PG type to Oracle type
                    oracle_type = PG_TO_ORACLE_TYPES.get(pg_type, "VARCHAR2")  # default to VARCHAR2

                    self.param_types.append(oracle_type)
        
        # Start building procedure header
        param_decls = ", ".join(
            f"{name} IN {ptype}" for name, ptype in zip(self.param_names, self.param_types)
        )
        header = f"CREATE OR REPLACE PROCEDURE {self.proc_name}({param_decls}) IS\n"
        
        # Visit the body
        body_ctx = ctx.createfunc_opt_list()
        body_str = ""
        if body_ctx:
            # Find the AS clause with the procedure body as a string literal
            for opt in body_ctx.createfunc_opt_item():
                if opt.getText().startswith("AS"):
                    # Extract the raw body text (strip $procedure$ etc.)
                    func_as_ctx = opt.func_as()
                    raw_body = func_as_ctx.sconst(0).getText()

                    # Remove dollar quoting delimiters (e.g. $procedure$)
                    body = raw_body.strip("'\"$procedure$\r\n ")
                    
                    # Replace $1, $2 etc. with param names
                    for i, pname in enumerate(self.param_names, 1):
                        body = body.replace(f"${i}", pname)
                    
                    # Convert RAISE NOTICE -> DBMS_OUTPUT.PUT_LINE
                    import re
                    body = re.sub(r"RAISE\s+NOTICE\s+'([^']*)';", r"DBMS_OUTPUT.PUT_LINE('\1');", body, flags=re.IGNORECASE)
                    
                    body_str = body
                    break
        
        # Combine full procedure text

        match = re.fullmatch(r"\s*BEGIN\s*(.*?)\s*END;\s*", body_str, re.IGNORECASE | re.DOTALL)
        if match:
            inner_body = match.group(1).strip()
            body_str = "BEGIN\n" + inner_body + "\n"
        else:
        # If no match, still wrap with BEGIN to be safe
            body_str = "BEGIN\n" + body_str.strip() + "\n"

        proc_text = header + body_str + "\nEND;\n/"
        return proc_text


# To use:

def convert_pg_to_oracle(sql_text):
    from antlr4 import InputStream, CommonTokenStream
    from antlr.PostgreSQLLexer import PostgreSQLLexer
    from antlr.PostgreSQLParser import PostgreSQLParser

    input_stream = InputStream(sql_text)
    lexer = PostgreSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PostgreSQLParser(stream)
    tree = parser.createfunctionstmt()  # parse the procedure
    
    visitor = PgToOracleVisitor()
    oracle_proc = visitor.visit(tree)
    return oracle_proc

# Example:

# if __name__ == "__main__":
#     pg_proc = """
#     CREATE PROCEDURE insert_test(IN numeric, IN character varying)
#     LANGUAGE plpgsql
#     AS $procedure$
#     BEGIN
#         RAISE NOTICE 'Inserting record';
#         INSERT INTO test_proc (id, name) VALUES ($1, $2);
#         COMMIT;
#     END;
#     $procedure$;
#     """







# with open("examples/fin_test1.sql", "r", encoding="utf-8") as f:
#     pg_proc = f.read()
    
# con = convert_pg_to_oracle(pg_proc)


# output_path = r"c:\Users\PrashantKumar\Desktop\sql-wizard\output\out1test.sql"

# with open(output_path, "w", encoding="utf-8") as f:
#     f.write(con)

# print(f"Oracle SQL procedure written to {output_path}")
