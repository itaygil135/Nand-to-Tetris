"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

VM_SEGMENT_CONST_STR = "constant"
VM_SEGMENT_ARG_STR  = "argument"
VM_SEGMENT_LOCAL_STR  ="local"
VM_SEGMENT_STATIC_STR  = "static"
VM_SEGMENT_THIS_STR  = "this"
VM_SEGMEN_THAT_STR  = "that"
VM_SEGMENT_POINTER_STR  = "pointer"
VM_SEGMENT_TEMP_STR  = "temp"

VM_SEGMENT_CONST = "CONST"
VM_SEGMENT_ARG = "ARG"
VM_SEGMENT_LOCAL ="LOCAL"
VM_SEGMENT_STATIC = "STATIC"
VM_SEGMENT_THIS = "THIS"
VM_SEGMEN_THAT = "THAT"
VM_SEGMENT_POINTER = "POINTER"
VM_SEGMENT_TEMP = "TEMP"


# mapping from symbol table terms to VM grammar terms
VM_SEGMENTS = { VM_SEGMENT_CONST: VM_SEGMENT_CONST_STR,
                VM_SEGMENT_ARG:VM_SEGMENT_ARG_STR,
                VM_SEGMENT_LOCAL:VM_SEGMENT_LOCAL_STR,
                VM_SEGMENT_STATIC: VM_SEGMENT_STATIC_STR,
                VM_SEGMENT_THIS: VM_SEGMENT_THIS_STR,
                VM_SEGMEN_THAT: VM_SEGMEN_THAT_STR,
                VM_SEGMENT_POINTER: VM_SEGMENT_POINTER_STR,
                VM_SEGMENT_TEMP: VM_SEGMENT_TEMP_STR }



COMMANDS_TO_VM_COMMANDS = {"NEG": "neg" ,
                           "NOT": "not",
                           "SHIFTLEFT": "shiftleft",
                           "SHIFTRIGHT": "shiftright",
                           "ADD": "add",
                           "SUB": "sub",
                           "EQ": "eq",
                           "LT": "lt",
                           "GT": "gt",
                           "AND": "and",
                           "OR": "or" }

class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.num_of_tabs = 0

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("push " +
                                 VM_SEGMENTS[segment] +
                                 " " +
                                 str(index) +
                                 "\n")

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("pop " +
                                 VM_SEGMENTS[segment] +
                                 " " +
                                 str(index) +
                                 "\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        # Your code goes here!
        #todo - translate to VM grammar
        #l_command = command.lower()
        l_command = COMMANDS_TO_VM_COMMANDS[command]
        self.write_tabs()
        self.output_stream.write(l_command +
                                 "\n")

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("label " +
                                 f"{label}" +
                                 "\n")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("goto " +
                                 f"{label}" +
                                 "\n")

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("if-goto " +
                                 f"{label}" +
                                 "\n")

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("call " +
                                 f"{name}" +
                                 " " +
                                 str(n_args) +
                                 "\n")
        pass

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("function " +
                                 f"{name}" +
                                 " " +
                                 str(n_locals) +
                                 "\n")

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.write_tabs()
        self.output_stream.write("return " +
                                 "\n")

    def write_jack_comment(self, comment:str) -> None:
        return
        if comment != "":
            header = "    // "  + comment
        self.write_tabs()
        self.output_stream.write(header + "\n")

    def write_jack_command_header(self, comment: str, shift: int) -> None:
        return
        " write comment at the beginning of jack command flow"
        if shift < 0:
            self.num_of_tabs -= 1
        elif shift > 0:
            self.num_of_tabs += 1
        header = ""
        if comment != "":
            header = "//------ "  + comment
        self.write_tabs()
        self.output_stream.write(header + "\n")


    def write_tabs(self) -> None:
        return
        for i in range(self.num_of_tabs):
            self.output_stream.write("  ")


