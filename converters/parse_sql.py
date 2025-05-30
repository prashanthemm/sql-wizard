# from antlr4 import *
# from antlr.PostgreSQLLexer import PostgreSQLLexer
# from antlr.PostgreSQLParser import PostgreSQLParser

# def parse_sql_file(filename):
#     input_stream = FileStream(filename, encoding='utf-8')
#     lexer = PostgreSQLLexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = PostgreSQLParser(stream)

#     tree = parser.stmt()
#     print(tree.toStringTree(recog=parser))  # Just for testing

# parse_sql_file("input_extraction/demo1.sql")
