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
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION",
C_RETURN = "C_RETURN"
C_CALL ="C_CALL"
C_SHIFT = "C_SHIFT"
C_ILLEGAL = ""

class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """


    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.input_lines_arr = input_file.read().splitlines()  # Array of file lines
        self.strip_all_line()
        self.cur_line = FIRST_LINE
        self.current_command = FIRST_COMMAND

    def strip_all_line(self):
        for i in range(len(self.input_lines_arr)):
            line = self.input_lines_arr[i]

        line1 = line.strip()  # remove white spaces at the begining and end
                              # of the line
        self.input_lines_arr[i] = line1.split(COMMENT)[0] # remove comments

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
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
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
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        if self.current_command.split()[0] == "push":
            return C_PUSH
        elif self.current_command.split()[0] == "pop":
            return C_POP
        elif self.current_command.split()[0] == "label":
            return C_LABEL
        elif self.current_command.split()[0] == "goto":
            return C_GOTO
        elif self.current_command.split()[0] == "if-goto":
            return C_IF
        elif self.current_command.split()[0] == "function":
            return C_FUNCTION
        elif self.current_command.split()[0] == "return":
            return C_RETURN
        elif self.current_command.split()[0] == "call":
            return C_CALL
        elif self.current_command.split()[0] == "shiftleft":
            return C_SHIFT
        elif self.current_command.split()[0] == "shiftright":
            return C_SHIFT
        elif self.current_command.split()[0] == "add":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "sub":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "neg":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "eq":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "gt":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "lt":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "and":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "or":
            return C_ARITHMETIC
        elif self.current_command.split()[0] == "not":
            return C_ARITHMETIC
        return C_ILLEGAL

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        if self.command_type() == C_ARITHMETIC or self.command_type() == C_SHIFT:
            return self.current_command.split()[0]
        return self.current_command.split()[1]


    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        return self.current_command.split()[2]

    def _is_whitespace(self, line):
        if line == "" or line.isspace() or line[0:2] == COMMENT:
            return True
        return False