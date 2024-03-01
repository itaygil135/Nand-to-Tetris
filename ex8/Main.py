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
from Parser import Parser
from CodeWriter import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION",
C_RETURN = "C_RETURN"
C_CALL ="C_CALL"
C_SHIFT="C_SHIFT"
C_ILLEGAL = ""
FIRST_CODE_LINE = 0


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the
            first file we are translating.
    """
    # Your code goes here!
    # It might be good to start with something like:
    # parser = Parser(input_file)
    # code_writer = CodeWriter(output_file)
    parser = Parser(input_file)
    codeWriter = CodeWriter(output_file)

    input_file_name =os.path.basename(input_file.name).split(".")[0]
    codeWriter.set_file_name(input_file_name)

    if bootstrap == True:
        codeWriter.write_bootstrap()

    input_file.seek(0)
    current_code_line = FIRST_CODE_LINE
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        arg1 = parser.arg1();

        if command_type == C_ARITHMETIC or command_type == C_SHIFT:
            codeWriter.write_arithmetic(arg1)
        elif command_type == C_POP or command_type == C_PUSH:
            arg2 = int(parser.arg2());
            codeWriter.write_push_pop(command_type, arg1, arg2)
        elif command_type == C_IF:
            codeWriter.write_if(arg1)
        elif command_type == C_GOTO:
            codeWriter.write_goto(arg1)
        elif command_type == C_LABEL:
            codeWriter.write_label(arg1)
        elif command_type == C_RETURN:
            codeWriter.write_return()
        elif command_type == C_CALL:
            arg2 = int(parser.arg2());
            codeWriter.write_call(arg1, arg2)
        elif command_type == C_FUNCTION:
            arg2 = int(parser.arg2());
            codeWriter.write_function(arg1, arg2)

if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:

        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
                bootstrap = False
            input_file.close()
    output_file.close()
