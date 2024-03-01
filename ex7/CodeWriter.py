"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION",
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"
C_SHIFT="C_SHIFT"
C_ILLEGAL = ""

ARG_SEGMENT = "argument"
LOCAL_SEGMENT = "local"
THIS_SEGMENT = "this"
THAT_SEGMENT = "that"
CONST_SEGMENT = "constant"
STATIC_SEGMENT = "static"
TEMP_SEGMENT = "temp"
TEMP_SEGMENT_START = 5
POINTERS_SEGMENT = "pointer"
POINTERS = {0: "THIS", 1: "THAT"}


FIRST_SEGMENTS = {ARG_SEGMENT: "ARG", LOCAL_SEGMENT: "LCL", THIS_SEGMENT: "THIS", THAT_SEGMENT: "THAT"}


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.outputFile = output_stream
        self.fileName = ""
        self.eq_count = 0
        self.gt_count = 0
        self.lt_count = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.fileName = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        self.outputFile.write("\n" + f"// execute command: {command}" + "\n")
        if command == "add":
            operation_str = "+"
            self.write_binary_flow(operation_str)
        elif command == "sub":
            operation_str = "-"
            self.write_binary_flow(operation_str)
        elif command == "and":
            operation_str = "&"
            self.write_binary_flow(operation_str)
        elif command == "or":
            operation_str = "|"
            self.write_binary_flow(operation_str)
        elif command == "eq":
            self.write_eq_flow()
        elif command == "gt":
            self.write_gt_flow()
        elif command == "lt":
            self.write_lt_flow()
        elif command == "neg":
            m_operation_str = "-M"
            self.write_unary_flow(m_operation_str)
        elif command == "not":
            m_operation_str = "!M"
            self.write_unary_flow(m_operation_str)
        elif command == "shiftleft":
            m_operation_str = "M<<"
            self.write_unary_flow(m_operation_str)
        elif command == "shiftright":
            m_operation_str = "M>>"
            self.write_unary_flow(m_operation_str)

    def write_unary_flow(self, m_operation_str):
        self.outputFile.write("@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=" + m_operation_str + "\n")

    def write_binary_flow(self, operation_str):
        self.outputFile.write("@SP" + "\n" +
                              "M=M-1" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              "A=A-1" + "\n" +
                              "M=M" + operation_str + "D" + "\n")

    def write_eq_flow(self) -> None:
        self.eq_count = self.eq_count + 1
        self.outputFile.write("@32767" + "\n" +
                              "D=!A" + "\n" +
                              "@R14" + "\n" +
                              "M=D" + "\n" +
                              "@R15" + "\n" +
                              "M=D" + "\n" +
                              "@SP" + "\n" +
                              "AM=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "M=D&M" + "\n" +
                              "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R15" + "\n" +
                              "M=D&M" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "D=D-M" + "\n" +
                              f"@NOT_EQ{self.eq_count}" + "\n" +
                              "D;JNE" + "\n" +
                              "@SP" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              "A=A-1" + "\n" +
                              "D=D-M" + "\n" +
                              f"@EQUAL{self.eq_count}" + "\n" +
                              "D;JEQ" + "\n" +
                              f"(NOT_EQ{self.eq_count})" + "\n"
                                                           "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=0" + "\n" +
                              f"@END_EQ{self.eq_count}" + "\n" +
                              "0;JMP" + "\n"
                                        f"(EQUAL{self.eq_count})" + "\n"
                                                                    "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=-1" + "\n" +
                              f"(END_EQ{self.eq_count})" + "\n")

    def write_lt_flow(self) -> None:
        self.lt_count = self.lt_count + 1
        self.outputFile.write(f"// extrat bit 15 from sp(-1) and sp(-2)" +
                              "\n" +
                              "@32767" + "\n" +
                              "D=!A" + "\n" +
                              "@R14" + "\n" +
                              "M=D" + "\n" +
                              "@R15" + "\n" +
                              "M=D" + "\n" +
                              "@SP" + "\n" +
                              "AM=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "M=D&M" + "\n" +
                              "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R15" + "\n" +
                              "M=D&M" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "D=D-M" + "\n" +
                              f"@LT_DIFF_SIGN{self.lt_count}" + "\n" +
                              "D;JNE" + "\n" +
                              "@SP" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              "A=A-1" + "\n" +
                              "D=D-M" + "\n" +
                              f"@LT_GREATER_THAN{self.lt_count}" + "\n" +
                              "D;JLE" + "\n" +
                              f"@LT_LESSER_THAN{self.lt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(LT_DIFF_SIGN{self.lt_count})" + "\n"
                                                                 "@SP" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              f"@LT_LESSER_THAN{self.lt_count}" + "\n" +
                              "D;JGE" + "\n" +
                              f"@LT_GREATER_THAN{self.lt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(LT_LESSER_THAN{self.lt_count})" + "\n"
                                                                   "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=-1" + "\n" +
                              f"@END_LT{self.lt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(LT_GREATER_THAN{self.lt_count})" + "\n"
                                                                    "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=0" + "\n" +
                              f"@END_LT{self.lt_count}" + "\n" +
                              "0;JMP" + "\n" +
                              f"(END_LT{self.lt_count})" + "\n")

    def write_gt_flow(self) -> None:
        self.gt_count = self.gt_count + 1
        self.outputFile.write(f"// extrat bit 15 from sp(-1) and sp(-2)" +
                              "\n" +
                              "@32767" + "\n" +
                              "D=!A" + "\n" +
                              "@R14" + "\n" +
                              "M=D" + "\n" +
                              "@R15" + "\n" +
                              "M=D" + "\n" +
                              "@SP" + "\n" +
                              "AM=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "M=D&M" + "\n" +
                              "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "D=M" + "\n" +
                              "@R15" + "\n" +
                              "M=D&M" + "\n" +
                              "D=M" + "\n" +
                              "@R14" + "\n" +
                              "D=D-M" + "\n" +
                              f"@GT_DIFF_SIGN{self.gt_count}" + "\n" +
                              "D;JNE" + "\n" +
                              "@SP" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              "A=A-1" + "\n" +
                              "D=D-M" + "\n" +
                              f"@GT_GREATER_THAN{self.gt_count}" + "\n" +
                              "D;JLT" + "\n" +
                              f"@GT_LESSER_THAN{self.gt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(GT_DIFF_SIGN{self.gt_count})" + "\n"
                                                                 "@SP" + "\n" +
                              "A=M" + "\n" +
                              "D=M" + "\n" +
                              f"@GT_LESSER_THAN{self.gt_count}" + "\n" +
                              "D;JGE" + "\n" +
                              f"@GT_GREATER_THAN{self.gt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(GT_LESSER_THAN{self.gt_count})" + "\n"
                                                                   "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=0" + "\n" +
                              f"@END_GT{self.gt_count}" + "\n" +
                              "0;JMP" + "\n" + "\n" +
                              f"(GT_GREATER_THAN{self.gt_count})" + "\n"
                                                                    "@SP" + "\n" +
                              "A=M-1" + "\n" +
                              "M=-1" + "\n" +
                              f"@END_GT{self.gt_count}" + "\n" +
                              "0;JMP" + "\n" +
                              f"(END_GT{self.gt_count})" + "\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        self.outputFile.write("\n" + f"// execute command: {command}" +
                              f"  {segment} " + str(index) + "\n")
        if command == C_PUSH:
            self.push_command(segment, index)
        if command == C_POP:
            self.pop_command(segment, index)

    def push_command(self, segment: str, index: int) -> None:
        if segment in FIRST_SEGMENTS.keys():
            segment_str = FIRST_SEGMENTS[segment]
            self.outputFile.write("@" + segment_str + "\n" +
                                  "D=M" + "\n" +
                                  "@" + str(index) + "\n" +
                                  "A=D+A" + "\n" +
                                  "D=M" + "\n" +
                                  "@SP" + "\n" +
                                  "A=M" + "\n" +
                                  "M=D" + "\n" +
                                  "@SP" + "\n" +
                                  "M=M+1" + "\n")
        elif segment == STATIC_SEGMENT:
            segment_str = self.fileName + '.' + str(index)
            self.outputFile.write("@" + segment_str + "\n" +
                                  # store the value from the relative address
                                  "D=M" + "\n" +
                                  # point to the top of the stack
                                  "@SP" + "\n" +
                                  "A=M" + "\n" +
                                  # push the value to the stack
                                  "M=D" + "\n" +
                                  # increase the stack pointer
                                  "@SP" + "\n" +
                                  "M=M+1" + "\n")
        elif segment == TEMP_SEGMENT:
            temp_pos = TEMP_SEGMENT_START + index
            segment_str = str(temp_pos)
            self.outputFile.write("@" + segment_str + "\n" +
                                  # store the value from the relative address
                                  "D=M" + "\n" +
                                  # point to the top of the stack
                                  "@SP" + "\n" +
                                  "A=M" + "\n" +
                                  # push the value to the stack
                                  "M=D" + "\n" +
                                  # increase the stack pointer
                                  "@SP" + "\n" +
                                  "M=M+1" + "\n")
        elif segment == CONST_SEGMENT:
            index_str = str(index)
            self.outputFile.write("@" + index_str + "\n" +  # starting address
                                  # store the addres as value
                                  "D=A" + "\n" +
                                  # point to the top of the stack
                                  "@SP" + "\n" +
                                  "A=M" + "\n" +
                                  # push the value to the stack
                                  "M=D" + "\n" +
                                  # increase the stack pointer
                                  "@SP" + "\n" +
                                  "M=M+1" + "\n")
        elif segment == POINTERS_SEGMENT:
            segment_str = str(POINTERS[index])
            self.outputFile.write(f"@{segment_str}" + "\n" +
                              "D=M" + "\n" +
                              "@SP" + "\n" +
                              "M=M+1" + "\n" +
                              "A=M-1" + "\n" +
                              "M=D" + "\n")


    def pop_command(self, segment: str, index: int) -> None:
        if segment in FIRST_SEGMENTS.keys():
            segment_str = FIRST_SEGMENTS[segment]
            self.outputFile.write("@" + segment_str + "\n" +
                                  "D=M" + "\n" +
                                  "@" + str(index) + "\n" +
                                  "D=D+A" + "\n" +
                                  "@R13" + "\n" +
                                  "M=D" + "\n" +
                                  "@SP" + "\n" +
                                  "M=M-1" + "\n" +
                                  "A=M" + "\n" +
                                  "D=M" + "\n" +
                                  "@R13" + "\n" +
                                  "A=M" + "\n" +
                                  "M=D" + "\n")
        elif segment == STATIC_SEGMENT:
            segment_str = self.fileName + '.' + str(index)
            self.outputFile.write("@" + segment_str + "\n" +
                                  "D=A" + "\n" +
                                  "@R13" + "\n" +
                                  "M=D" + "\n" +
                                  "@SP" + "\n" +
                                  "M=M-1" + "\n" +
                                  "A=M" + "\n" +
                                  "D=M" + "\n" +
                                  "@R13" + "\n" +
                                  "A=M" + "\n" +
                                  "M=D" + "\n")
        elif segment == TEMP_SEGMENT:

            temp_pos = TEMP_SEGMENT_START + index
            segment_str = str(temp_pos)
            self.outputFile.write("@" + segment_str + "\n" +
                                  "D=A" + "\n" +
                                  "@R13" + "\n" +
                                  "M=D" + "\n" +
                                  "@SP" + "\n" +
                                  "M=M-1" + "\n" +
                                  "A=M" + "\n" +
                                  "D=M" + "\n" +
                                  "@R13" + "\n" +
                                  "A=M" + "\n" +
                                  "M=D" + "\n")
        elif segment == POINTERS_SEGMENT:
            segment_str = str(POINTERS[index])
            self.outputFile.write("@SP" + "\n" +
                              "AM=M-1" + "\n" +
                              "D=M" + "\n" +
                              f"@{segment_str}" + "\n" +
                              "M=D" + "\n")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
