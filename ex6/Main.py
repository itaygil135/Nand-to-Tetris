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
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


A_COMMAND = "A_COMMAND"
L_COMMAND = "L_COMMAND"
C_COMMAND = "C_COMMAND"
FIRST_COD_LINE = 0
ILLEGAL_ADDRESS = -1
REGISTER_LEN = 16


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """

    symbol_table = SymbolTable()

    # first pass:
    scan_labels(symbol_table)

    # second pass:
    parse_command(input_file, output_file, symbol_table)

    input_file.close()
    output_file.close()


def parse_command(input_file, output_file, symbol_table):
    parser = Parser(input_file)
    code = Code()
    n = 16
    input_file.seek(0)
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == A_COMMAND:
            n = parse_a_command(n, output_file, parser, symbol_table)
        elif parser.command_type() == C_COMMAND:
            n = parse_c_command(n,code, output_file, parser)


def parse_c_command(n,code, output_file, parser):
    dest_bin = code.dest(parser.dest())
    comp_bin = code.comp(parser.comp())
    jump_bin = code.jump(parser.jump())
    if parser.is_shift():
        shift_bin = "101"
    else:
        shift_bin = "111"
    new_input = shift_bin + comp_bin + dest_bin + jump_bin + "\n"
    output_file.write(new_input)
    return n


def parse_a_command(n, output_file, parser, symbol_table):
    decimal_address = ILLEGAL_ADDRESS
    new_symbol = parser.symbol()
    if new_symbol.isdigit():
        decimal_address = int(new_symbol)
    else:
        if not symbol_table.contains(new_symbol):
            symbol_table.add_entry(new_symbol, n)
            n += 1
        decimal_address = symbol_table.get_address(new_symbol)

    bin_address = (str(bin(decimal_address)))[2:]
    new_output = "0" * (REGISTER_LEN - len(bin_address)) + bin_address
    output_file.write(new_output + "\n")
    return n


def scan_labels(symbol_table):
    parser = Parser(input_file)
    current_cod_line = FIRST_COD_LINE
    input_file.seek(0)
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == L_COMMAND:
            new_symbol = parser.symbol()
            symbol_table.add_entry(new_symbol, current_cod_line)
        else:
            current_cod_line += 1




if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
