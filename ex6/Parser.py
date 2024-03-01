"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

COMMENT = "//"
FIRST_LINE = 0
FIRST_COMMAND = ""
A_COMMAND = "A_COMMAND"
L_COMMAND = "L_COMMAND"
C_COMMAND = "C_COMMAND"
EQUAL = "="
EMPTY_STR = ""
SEMICOLON = ";"
SHIFT_R = ">>"
SHIFT_L = "<<"


class Parser:
    """Encapsulates access to the input code. Reads an assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        self.input_lines_arr = input_file.read().splitlines()  # Array of file lines
        self.strip_all_line()
        self.cur_line = FIRST_LINE
        self.current_command = FIRST_COMMAND



    def strip_all_line(self):
        for i in range(len(self.input_lines_arr)):
            line = self.input_lines_arr[i]
            line1= ''.join(line.split())
            self.input_lines_arr[i] = line1.split(COMMENT)[0]

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.cur_line == len(self.input_lines_arr):
            return False
        for line in self.input_lines_arr[self.cur_line:]:
            if not self._is_whitespace(line):
                return True
        return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
       #if not self.has_more_commands():
       #     return

        while self.cur_line < len(self.input_lines_arr):
            line = self.input_lines_arr[self.cur_line]
            if not self._is_whitespace(line):
                self.current_command = line
                self.cur_line += 1
                return
            self.cur_line += 1

        self.current_command = FIRST_COMMAND

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.current_command[0] == "@":
            return A_COMMAND
        if self.current_command[0] == "(":
            return L_COMMAND
        return C_COMMAND

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == A_COMMAND:
            return self.current_command[1:]
        if self.command_type() == L_COMMAND:
            return self.current_command[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if EQUAL in self.current_command:
            return self.current_command.split(EQUAL)[0]
        return EMPTY_STR

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        if EQUAL in self.current_command:
            x = self.current_command.split(EQUAL)[1]
            return x.split(SEMICOLON)[0]
        return self.current_command.split(SEMICOLON)[0]


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if SEMICOLON in self.current_command:
            return self.current_command.split(SEMICOLON)[1]
        return EMPTY_STR


    def _is_whitespace(self, line):
        if line == "" or line.isspace() or line[0:2] == COMMENT:
            return True
        return False

    def is_shift(self) -> bool:
        if SHIFT_R in self.current_command or SHIFT_L in self.current_command:
            return True
        return False

