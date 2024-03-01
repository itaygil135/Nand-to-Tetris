"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer

FIRST_CODE_LINE = 0
#token types
T_KEYWORD = "KEYWORD"
T_SYMBOL = "SYMBOL"
T_IDENTIFIER = "IDENTIFIER"
T_INT_CONST = "INT_CONST"
T_STRING_CONST = "STRING_CONST"
T_ILLEGAL = "ILLEGAL_TOKEN"

#token string
T_KEYWORD_STR = "keyword"
T_SYMBOL_STR  = "symbol"
T_IDENTIFIER_STR  = "identifier"
T_INT_CONST_STR  = "integerConstant"
T_STRING_CONST_STR  = "stringConstant"


def handle_token( tokenizer) -> None:
    token_type = tokenizer.token_type()
    if token_type == T_KEYWORD:
        token_str = T_KEYWORD_STR
        token_value_str = tokenizer.keyword()
    elif token_type == T_SYMBOL:
        token_str = T_SYMBOL_STR
        token_value_str = tokenizer.symbol()
    elif token_type == T_IDENTIFIER:
        token_str = T_IDENTIFIER_STR
        token_value_str = tokenizer.identifier()
    elif token_type == T_INT_CONST:
        token_str = T_INT_CONST_STR
        token_value_str = tokenizer.int_val()
    elif token_type == T_STRING_CONST:
        token_str = T_STRING_CONST_STR
        token_value_str= tokenizer.string_val()
    else:
        token_str = ""
        token_value_str = ""

    output_file.write("<" + \
                  token_str + \
                  "> " + \
                  token_value_str + \
                  " </" + \
                  token_str + \
                  ">" + "\n")



def analyze_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Analyzes a single file.

    Args:
        input_file (typing.TextIO): the file to analyze.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # It might be good to start by creating a new JackTokenizer and CompilationEngine:

    # stage1 is used to verify tokenizer code.
    #stage1(input_file,output_file)


    # stage2 is for subbmission
    stage2(input_file,output_file)

def stage2(input_file: typing.TextIO, output_file: typing.TextIO ) -> None:
    tokenizer = JackTokenizer(input_file)
    engine = CompilationEngine( tokenizer,output_file)

def stage1(input_file: typing.TextIO, output_file: typing.TextIO ) -> None:
    tokenizer = JackTokenizer(input_file)
    output_file.write("<tokens>" + "\n")
    input_file.seek(0)
    #  current_code_line = FIRST_CODE_LINE
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        handle_token(tokenizer)
    output_file.write("</tokens>" + "\n")


if "__main__" == __name__:
    # Parses the input path and calls analyze_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackAnalyzer <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        output_path = filename + ".xml"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            analyze_file(input_file, output_file)
            input_file.close()
            output_file.close()




