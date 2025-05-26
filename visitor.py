from antlr4 import *
from antlr.PostgreSQLLexer import PostgreSQLLexer
from antlr.PostgreSQLParser import PostgreSQLParser
from antlr.PostgreSQLParserVisitor import PostgreSQLParserVisitor

# Map PostgreSQL types to Oracle types (expand as needed)
PG_TO_ORACLE_TYPES = {
    "numeric": "NUMBER",
    "character varying": "VARCHAR2",
    "varchar": "VARCHAR2",
    "integer": "INTEGER",
    "boolean": "BOOLEAN",
    # Add more types here as needed
}

class PgToOracleVisitor(PostgreSQLParserVisitor):
    def __init__(self):
        super().__init__()
        self.proc_name = ""
        self.params = []
        self.body = ""

    def visitCreatefunctionstmt(self, ctx:PostgreSQLParser.CreatefunctionstmtContext):
        # Extract procedure name
        func_name_ctx = ctx.func_name()
        # Usually func_name -> type_function_name -> identifier
        self.proc_name = func_name_ctx.getText()  # You can customize deeper extraction if needed

        # Extract parameters
        if ctx.func_args_with_defaults():
            params_ctx = ctx.func_args_with_defaults().func_args_with_defaults_list()
            if params_ctx:
                self.visitFunc_args_with_defaults_list(params_ctx)

        # Extract procedure body (func_as)
        if ctx.createfunc_opt_list():
            for opt in ctx.createfunc_opt_list().createfunc_opt_item():
                if opt.LANGUAGE():
                    # Just detect LANGUAGE option, skip here
                    continue
                if opt.AS():
                    # opt.func_as() has the body
                    self.visitFunc_as(opt.func_as())

        return self  # or whatever you want

    def visitFunc_args_with_defaults_list(self, ctx:PostgreSQLParser.Func_args_with_defaults_listContext):
        params = []
        for param_ctx in ctx.func_arg_with_default():
            func_arg = param_ctx.func_arg()
            # Extract mode (IN, OUT, etc.)
            mode = func_arg.arg_class().getText() if func_arg.arg_class() else "IN"

            # Extract parameter name (optional)
            param_name = None
            if func_arg.param_name():
                param_name = func_arg.param_name().getText()

            # Extract type name (go deeper)
            type_name = ""
            if func_arg.func_type():
                type_name = func_arg.func_type().typename().getText()

            params.append({"mode": mode, "name": param_name, "type": type_name})
        self.params = params
        return params

    def visitFunc_as(self, ctx:PostgreSQLParser.Func_asContext):
        # Extract raw body text (it includes $procedure$ delimiters)
        body_text = ctx.sconst(0).getText()
        # Remove $procedure$ delimiters if present
        if body_text.startswith("$procedure$") and body_text.endswith("$procedure$"):
            body_text = body_text[len("$procedure$"):-len("$procedure$")].strip()
        self.body = body_text
        return self.body

    def format_params(self):
        formatted_params = []
        for p in self.params:
            name = p['name'] if p['name'] else "param"
            oracle_type = PG_TO_ORACLE_TYPES.get(p['type'].lower(), "VARCHAR2")
            mode = p['mode'].upper()
            formatted_params.append(f"{name} {mode} {oracle_type}")
        return ", ".join(formatted_params)

    def to_oracle_procedure(self):
        header = f"CREATE OR REPLACE PROCEDURE {self.proc_name} ({self.format_params()}) IS\nBEGIN\n"
        body = self.body + "\nEND;\n/"
        return header + body


def parse_and_convert_pg_proc(input_sql_text):
    input_stream = InputStream(input_sql_text)
    lexer = PostgreSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PostgreSQLParser(stream)
    tree = parser.stmt()  # parse the SQL as a statement

    visitor = PgToOracleVisitor()
    visitor.visit(tree)
    return visitor.to_oracle_procedure()


if __name__ == "__main__":
    sample_pg_proc = """
    CREATE PROCEDURE insert_test(IN numeric, IN character varying)
    LANGUAGE plpgsql
    AS $procedure$
    BEGIN
        INSERT INTO test_proc (id, name) VALUES ($1, $2);
        COMMIT;
    END;
    $procedure$;
    """

    oracle_proc = parse_and_convert_pg_proc(sample_pg_proc)
    print("Converted Oracle Procedure:\n")
    print(oracle_proc)
