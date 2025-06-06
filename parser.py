from antlr4 import *
from antlr.PostgreSQLLexer import PostgreSQLLexer
from antlr.PostgreSQLParser import PostgreSQLParser
from antlr.PostgreSQLParserVisitor import PostgreSQLParserVisitor
import json
import os
import logging


log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# logging configuration
logger = logging.getLogger('parser.log')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(log_dir, 'parser.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class PgToOracleVisitor(PostgreSQLParserVisitor):
    def __init__(self):
        super().__init__()
        self.param_names = []
        self.param_types = []
        self.proc_name = ""
    
    def visitCreatefunctionstmt(self, ctx):
        """Translation logic"""
        try:
            self.proc_name = ctx.func_name().getText()
            
            with open(os.path.join("rules", "types_maps.json"), "r") as f:
                PG_TO_ORACLE_TYPES = json.load(f)
            
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
            param_decls = ", ".join(
                f"{name} IN {ptype}" for name, ptype in zip(self.param_names, self.param_types)
            )
            header = f"CREATE OR REPLACE PROCEDURE {self.proc_name}({param_decls}) IS\n"
            body_ctx = ctx.createfunc_opt_list()
            body_str = ""
            if body_ctx:
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

            match = re.fullmatch(r"\s*BEGIN\s*(.*?)\s*END;\s*", body_str, re.IGNORECASE | re.DOTALL)
            if match:
                inner_body = match.group(1).strip()
                body_str = "BEGIN\n" + inner_body + "\n"
            else:
            # If no match, still wrap with BEGIN to be safe
                body_str = "BEGIN\n" + body_str.strip() + "\n"

            proc_text = header + body_str + "\nEND;\n/"
            logger.debug('Inside Parser - Conversion happened')
            return proc_text
        
        
        except Exception as e:
            logger.error('Inside Parser - Conversion to oracle syntax failed: %s', e)





def convert_pg_to_oracle(sql_text):
    try:
        from antlr4 import InputStream, CommonTokenStream
        from antlr.PostgreSQLLexer import PostgreSQLLexer
        from antlr.PostgreSQLParser import PostgreSQLParser

        input_stream = InputStream(sql_text)
        lexer = PostgreSQLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PostgreSQLParser(stream)
        tree = parser.createfunctionstmt()  # parse the procedure
        logger.debug('Inside Parser - Translation to oracle syntax started')    
        visitor = PgToOracleVisitor()
        oracle_proc = visitor.visit(tree)
        logger.debug('Inside Parser - Translation is done into oracle syntax')
        return oracle_proc
    except Exception as e:
        logger.error('Inside Parser - Translation did not begin: %s', e)
        raise



