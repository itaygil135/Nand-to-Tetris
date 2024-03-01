"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

# tokenaizer related definitions
# token types
T_KEYWORD = "KEYWORD"
T_SYMBOL = "SYMBOL"
T_IDENTIFIER = "IDENTIFIER"
T_INT_CONST = "INT_CONST"
T_STRING_CONST = "STRING_CONST"

# token string
T_KEYWORD_STR = "keyword"
T_SYMBOL_STR = "symbol"
T_IDENTIFIER_STR = "identifier"
T_INT_CONST_STR = "integerConstant"
T_STRING_CONST_STR = "stringConstant"

TOKEN_TYPES_STRINGS = {T_KEYWORD: T_KEYWORD_STR,
                       T_SYMBOL: T_SYMBOL_STR,
                       T_IDENTIFIER: T_IDENTIFIER_STR,
                       T_INT_CONST: T_INT_CONST_STR,
                       T_STRING_CONST: T_STRING_CONST_STR}

# symbol table related definitions
FIELD_KIND = "FIELD"
STATIC_KIND = "STATIC"
ARG_KIND = "ARG"
VAR_KIND = "VAR"

# VM grammar related definitions

VM_SEGMENT_CONST = "CONST"
VM_SEGMENT_ARG = "ARG"
VM_SEGMENT_LOCAL = "LOCAL"
VM_SEGMENT_STATIC = "STATIC"
VM_SEGMENT_THIS = "THIS"
VM_SEGMENT_THAT = "THAT"
VM_SEGMENT_POINTER = "POINTER"
VM_SEGMENT_TEMP = "TEMP"


# mapping from symbol table terms to VM grammar terms
JACK_KINDS_TO_VM_SEGMENTS = {FIELD_KIND: VM_SEGMENT_THIS,
                             STATIC_KIND: VM_SEGMENT_STATIC,
                             ARG_KIND: VM_SEGMENT_ARG,
                             VAR_KIND: VM_SEGMENT_LOCAL}

# JACK grammar related definitions
CLASS_VAR_DEC_SET = {'static', 'field'}

SUBRUOTINE_DEC_SET = {'constructor', 'function', 'method'}

# keywords for constants
KEYWORD_TRUE = "true"
KEYWORD_FALSE= "false"
KEYWORD_NULL = "null"
KEYWORD_THIS = "this"
KEYWORD_CONSTANT_SET = {KEYWORD_TRUE, KEYWORD_FALSE, KEYWORD_NULL, KEYWORD_THIS}

# symbols and mapping to commands
COMMAND_NEG = "NEG"
COMMAND_NOT = "NOT"
COMMAND_SHIFTLEFT = "SHIFTLEFT"
COMMAND_SHIFTRIGHT = "SHIFTRIGHT"
COMMAND_ADD = "ADD"
COMMAND_SUB = "SUB"
COMMAND_EQ = "EQ"
COMMAND_LG = "LT"
COMMAND_GT = "GT"
COMMAND_AND = "AND"
COMMAND_OR = "OR"

SYMBOL_PLUS = "+"
SYMBOL_MINUS = "-"
SYMBOL_ASTERISK = "*"
SYMBOL_SLASH = "/"
SYMBOL_AMP = "&"
SYMBOL_PIPE= "|"
SYMBOL_LT = "<"
SYMBOL_GT = ">"
SYMBOL_EQ = "="
SYMBOL_TILDE = "~"
SYMBOL_HASH = "#"
SYMBOL_HAT = "^"

OP_SET = {SYMBOL_PLUS, SYMBOL_MINUS, SYMBOL_ASTERISK, SYMBOL_SLASH,
          SYMBOL_AMP, SYMBOL_PIPE, SYMBOL_LT, SYMBOL_GT, SYMBOL_EQ }

UNARY_OP_SET = {SYMBOL_MINUS, SYMBOL_TILDE, SYMBOL_HAT, SYMBOL_HASH}

JACK_TO_VM_UNARY_COMMANDS = {SYMBOL_MINUS: COMMAND_NEG,
                             SYMBOL_TILDE: COMMAND_NOT,
                             SYMBOL_HAT: COMMAND_SHIFTLEFT,
                             SYMBOL_HASH: COMMAND_SHIFTRIGHT}

JACK_TO_VM_BINARY_COMMANDS = { SYMBOL_PLUS: COMMAND_ADD,
                               SYMBOL_MINUS: COMMAND_SUB,
                               SYMBOL_EQ: COMMAND_EQ,
                               SYMBOL_LT: COMMAND_LG,
                               SYMBOL_GT: COMMAND_GT,
                               SYMBOL_AMP: COMMAND_AND,
                               SYMBOL_PIPE: COMMAND_OR}

JACK_TO_VM_MATH_COMMANDS = {SYMBOL_ASTERISK: "Math.multiply",
                            SYMBOL_SLASH: "Math.divide"}

# todo handle the symbol " ->> &quot;

IF_FALSE_LABEL = "IF_FALSE"
IF_TRUE_LABEL = "IF_TRUE"
END_IF_LABEL = "IF_END"

START_WHILE_LABEL = "WHILE_EXP"
END_WHILE_LABEL = "WHILE_END"



class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")

        self.output_stream = output_stream
        self.tokenizer = input_stream
        self.vmwriter = VMWriter(output_stream)
        """ allocate defualt symbol tables, that actually will not be used
            since new objects will be allocated once class/subroutine 
            compilation starts
        """
        self.symbols = SymbolTable()
        self.symbols.set_output_stream(output_stream)
        self.num_of_tabs = 0
        self.class_name = ""
        self.if_counter = 0
        self.while_counter = 0

        """
        self.TOKEN_VALUE_STRINGS = {T_KEYWORD: self.tokenizer.keyword,
                                    T_SYMBOL: self.tokenizer.symbol,
                                    T_IDENTIFIER: self.tokenizer.identifier,
                                    T_INT_CONST: self.tokenizer.int_val,
                                    T_STRING_CONST: self.tokenizer.string_val}
                                    """
        self.compile_class()

    def eat(self, expected_token: str) -> None:
        # self.write_eat(expected_token()  # xml
        if expected_token != self.tokenizer.current_token_str:
            pass  # error case
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!

        self.print_xml_header("class", 1)
        self.eat("class")
        self.class_name = self.tokenizer.current_token_str
        self.vmwriter.write_jack_command_header(" compile_class " + self.class_name,1)  
        name = self.tokenizer.current_token_str
        var_type = ""
        var_kind = "CLASS"
        self.print_xml_class_subroutine_info(name, var_type, var_kind)
        self.eat(self.tokenizer.current_token_str)               # class name
        self.eat("{")

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in CLASS_VAR_DEC_SET:
                self.compile_class_var_dec()
            else:
                break

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in SUBRUOTINE_DEC_SET:
                self.compile_subroutine()
            else:
                break

        self.eat("}")
        self.vmwriter.write_jack_command_header("", -1)  
        self.print_xml_header("/class", -1)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        # self.compile_variables_declaration("classVarDec")
        self.print_xml_header("classVarDec", 1)
        # first mandatory variable
        kind = self.tokenizer.current_token_str.upper()
        self.eat(self.tokenizer.current_token_str)  # kind: "static" | "field"
        var_type = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # variable type
        name = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # variable name
        self.symbols.define(name, var_type, kind)
        self.print_xml_table_entry(name, True)

        # more variables
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == ',':
                self.eat(",")
                name = self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # variable name
                self.symbols.define(name, var_type, kind)
                self.print_xml_table_entry(name, True)
            else:
                break
        self.eat(";")
        self.print_xml_header("/" + "classVarDec", -1)

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.if_counter = 0
        self.while_counter = 0
        self.symbols.start_subroutine()
        self.print_xml_header("subroutineDec", 1)
        self.vmwriter.write_jack_command_header(" compile_subroutine ", 1)  

        func_type = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # constructor / function / method

        self.eat(self.tokenizer.current_token_str)  # void / type

        func_name = self.class_name + "." + self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # subroutine name

        if func_type == "method":
            name = KEYWORD_THIS
            kind = "ARG"
            var_type = self.class_name
            self.symbols.define(name, var_type, kind)
            self.print_xml_table_entry(name, True)

        # else:
            # self.sendWriter_xml_class_subroutine_info(name, type, kind)

        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.print_xml_header("subroutineBody", 1)
        self.eat("{")

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == 'var':
                self.compile_var_dec()
            else:
                break



        self.vmwriter.write_function(func_name,self.symbols.var_count(VAR_KIND))

        if func_type == "constructor":
            n_fields = self.symbols.var_count(FIELD_KIND)
            self.vmwriter.write_push(VM_SEGMENT_CONST, n_fields)
            self.vmwriter.write_call("Memory.alloc", 1)       # 1 is the number of arguments to the function Memory.alloc
            # update THIS to point to the new allocated memory
            self.vmwriter.write_pop (VM_SEGMENT_POINTER, 0)

        elif func_type == "method":
            # name = KEYWORD_THIS
            # kind = "ARG"
            # var_type = self.class_name
            # self.symbols.define(name, var_type, kind)
            # self.print_xml_table_entry(name, True)
            if func_type == "method":
                self.vmwriter.write_push(VM_SEGMENT_ARG, 0)
                self.vmwriter.write_pop(VM_SEGMENT_POINTER, 0)
        elif func_type == "function":
            pass



        self.compile_statements()
        self.eat("}")
        self.vmwriter.write_jack_command_header("", -1)  

        # todo - what about function that had no command return?  self.compile_return()
        self.print_xml_header("/subroutineBody", -1)
        self.print_xml_header("/subroutineDec", -1)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.print_xml_header("parameterList", 1)
        if self.tokenizer.current_token_str == ')':
            self.print_xml_header("/parameterList", -1)
            return
        var_type = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # parameter type
        name = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # parameter name
        kind = "ARG"
        self.symbols.define(name, var_type, kind)
        self.print_xml_table_entry(name, True)

        # more parameters
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == ',':
                self.eat(',')
                var_type = self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # parameter type
                name = self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # parameter name
                self.symbols.define(name, var_type, kind)
                self.print_xml_table_entry(name, True)
            else:
                break
        self.print_xml_header("/parameterList", -1)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!

        #  self.compile_variables_declaration("varDec")  # old code
        self.print_xml_header("varDec", 1)
        #  first mandatory variable
        self.eat(self.tokenizer.current_token_str)  # "var"
        var_type = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # variable type
        name = self.tokenizer.current_token_str
        self.eat(self.tokenizer.current_token_str)  # variable name

        kind = VAR_KIND
        self.symbols.define(name, var_type, kind)
        self.print_xml_table_entry(name, True)
        # more variables
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == ',':
                self.eat(",")
                name = self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # variable name
                self.symbols.define(name, var_type, kind)
                self.print_xml_table_entry(name, True)
            else:
                break
        self.eat(";")
        self.print_xml_header("/" + "varDec", -1)

    """
    def compile_variables_declaration(self, header_text: str):
        self.write_header(header_text, 1)
        # first mandatory variable
        self.eat(self.tokenizer.current_token_str)  # "var" / "static" /"field"
        self.eat(self.tokenizer.current_token_str)  # variable type
        self.eat(self.tokenizer.current_token_str)  # variable name
        # more variables
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == ',':
                self.eat(",")
                self.eat(self.tokenizer.current_token_str)  # variable name
            else:
                break
        self.eat(";")
        self.write_header("/"+header_text, -1)
    """

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.print_xml_header("statements", 1)
        while self.tokenizer.has_more_tokens():
            # todo - move to dic of statments and functions
            if self.tokenizer.current_token_str == 'let':
                self.compile_let()
            elif self.tokenizer.current_token_str == 'while':
                self.compile_while()
            elif self.tokenizer.current_token_str == 'do':
                self.compile_do()
            elif self.tokenizer.current_token_str == 'if':
                self.compile_if()
            elif self.tokenizer.current_token_str == 'return':
                self.compile_return()
            else:
                self.print_xml_header("/statements", -1)
                return

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.vmwriter.write_jack_command_header(" compile_let ", 1)
        self.print_xml_header("letStatement", 1)
        self.eat("let")
        var_kind = self.symbols.kind_of(self.tokenizer.current_token_str)
        var_index = self.symbols.index_of(self.tokenizer.current_token_str)
        self.print_xml_var_info(self.tokenizer.current_token_str)
        self.eat(self.tokenizer.current_token_str)
        if self.tokenizer.current_token_str == "[":
            #  self.vmwriter.write_jack_comment(" calculate THAT+index of the destination and keep it on the stack ")
            self.eat("[")
            self.compile_expression()
            self.vmwriter.write_push(JACK_KINDS_TO_VM_SEGMENTS[var_kind], var_index)
            self.vmwriter.write_arithmetic(COMMAND_ADD)
            self.eat("]")
            self.eat("=")
            #  self.vmwriter.write_jack_comment(" calculate value to assign ")
            self.compile_expression()
            self.vmwriter.write_pop(VM_SEGMENT_TEMP,0)  # store the returned value at temp 0 and remove it from the stack
            #   now the stack top is the original THAT+index
            #  self.vmwriter.write_jack_comment(" copy the THAT+index from stack top to the THAT pointer ")
            self.vmwriter.write_pop(VM_SEGMENT_POINTER, 1)  # 'set THAT pointer(address 4) to point to THAT+index
            #  self.vmwriter.write_jack_comment(" copy the stored return value to the stack top ")
            self.vmwriter.write_push(VM_SEGMENT_TEMP,0)  # copy the stored returned value form temp 0 to the stack
            #  self.vmwriter.write_jack_comment(" assign returned value to *THAT ")
            self.vmwriter.write_pop(VM_SEGMENT_THAT, 0)     # assign value into THAT+index (aka *THAT)

        else:
            self.eat("=")
            self.compile_expression()
            self.vmwriter.write_pop(JACK_KINDS_TO_VM_SEGMENTS[var_kind], var_index)
        self.eat(";")

        self.print_xml_header("/letStatement", -1)
        self.vmwriter.write_jack_command_header("", -1)  

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        counter = self.while_counter
        self.while_counter += 1
        self.vmwriter.write_jack_command_header(" compile_while ", 1)  
        self.print_xml_header("whileStatement", 1)
        start_while_label = START_WHILE_LABEL + str(counter)
        end_while_label = END_WHILE_LABEL + str(counter)
        self.eat("while")
        self.eat("(")
        self.vmwriter.write_label(start_while_label)
        self.compile_expression()
        self.vmwriter.write_arithmetic(COMMAND_NOT)
        self.vmwriter.write_if(end_while_label)  
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.vmwriter.write_goto(start_while_label)  
        self.vmwriter.write_label(end_while_label)
        self.print_xml_header("/whileStatement", -1)
        self.vmwriter.write_jack_command_header("", -1)


    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.vmwriter.write_jack_command_header(" compile_return ",1)  
        self.print_xml_header("returnStatement", 1)
        self.eat("return")
        if self.tokenizer.current_token_str != ';':
            self.compile_expression()
        else:
            self.vmwriter.write_push(VM_SEGMENT_CONST, 0)  
        self.eat(";")
        self.vmwriter.write_return()
        self.print_xml_header("/returnStatement", -1)
        self.vmwriter.write_jack_command_header("", -1)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        counter = self.if_counter
        self.if_counter += 1
        self.vmwriter.write_jack_command_header(" compile_if ", 1)
        self.print_xml_header("ifStatement", 1)
        if_false_label = IF_FALSE_LABEL + str(counter)
        end_if_label = END_IF_LABEL  + str(counter)
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.vmwriter.write_arithmetic(COMMAND_NOT)
        self.vmwriter.write_if(if_false_label)
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.vmwriter.write_goto(end_if_label)
        self.eat("}")
        self.vmwriter.write_label(if_false_label)
        if self.tokenizer.current_token_str == "else":
            self.vmwriter.write_jack_command_header(" handle else ", 0)
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
            #  self.vmwriter.write_jack_command_header("", 0)
        self.vmwriter.write_label(end_if_label)
        self.print_xml_header("/ifStatement", -1)
        self.vmwriter.write_jack_command_header("", -1)


    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!

        self.print_xml_header("expression", 1)
        # first term
        self.compile_term()
        # more terms
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in OP_SET:
                op = self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # op
                self.compile_term()  # next term
                if op in JACK_TO_VM_BINARY_COMMANDS:
                    self.vmwriter.write_arithmetic(JACK_TO_VM_BINARY_COMMANDS[op])
                elif op in JACK_TO_VM_MATH_COMMANDS:
                    self.vmwriter.write_call(JACK_TO_VM_MATH_COMMANDS[op], 2)
            else:
                break
        self.print_xml_header("/expression", -1)

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.print_xml_header("term", 1)
        if self.tokenizer.token_type() == T_INT_CONST:
            self.vmwriter.write_push(VM_SEGMENT_CONST, self.tokenizer.current_token_str)  
            self.eat(self.tokenizer.current_token_str)
        elif self.tokenizer.token_type() == T_STRING_CONST:
            # todo !!!!  self.vmwriter.write_push(?????, self.tokenizer.current_token_str)
            string_len = len(self.tokenizer.current_token_str) - 2
            self.vmwriter.write_push(VM_SEGMENT_CONST, string_len)
            self.vmwriter.write_call("String.new", 1)
            for letter in self.tokenizer.current_token_str[1:-1]:
                self.vmwriter.write_push(VM_SEGMENT_CONST, ord(letter))
                self.vmwriter.write_call("String.appendChar", 2)
            self.eat(self.tokenizer.current_token_str)

        elif self.tokenizer.current_token_str == KEYWORD_TRUE:
            self.vmwriter.write_push(VM_SEGMENT_CONST, 0)
            self.vmwriter.write_arithmetic(COMMAND_NOT)
            self.eat(self.tokenizer.current_token_str)
        elif self.tokenizer.current_token_str == KEYWORD_FALSE \
                or self.tokenizer.current_token_str == KEYWORD_NULL:
            self.vmwriter.write_push(VM_SEGMENT_CONST, 0)  
            self.eat(self.tokenizer.current_token_str)
        elif self.tokenizer.current_token_str == KEYWORD_THIS:
            self.vmwriter.write_push(VM_SEGMENT_POINTER, 0)  
            self.eat(self.tokenizer.current_token_str)

        elif self.tokenizer.current_token_str in UNARY_OP_SET:
            op = self.tokenizer.current_token_str
            self.eat(self.tokenizer.current_token_str)
            self.compile_term()
            self.vmwriter.write_arithmetic(JACK_TO_VM_UNARY_COMMANDS[op])
        elif self.tokenizer.current_token_str == "(":
            self.eat("(")
            self.compile_expression()
            self.eat(")")
        else:
            # eat var_name | var_name[] | subroutine_call
            self.print_xml_var_info(self.tokenizer.current_token_str)

            # option 1: the current token identifier is a var_name
            var_name = self.tokenizer.current_token_str

            # todo - the 'collect information' code is duplicate - can move it to a function
            # option 2 or 3: the current token identifier is an array or object of class name
            # collect information for the case of object or class call
            identifier_name = self.tokenizer.current_token_str
            identifier_kind = self.symbols.kind_of(identifier_name)
            if identifier_kind is not None:                     # known object
                identifier_type = self.symbols.type_of(identifier_name)
                identifier_index = self.symbols.index_of(identifier_name)
                callee_name = identifier_type
            else:                                               # unknown class
                callee_name = identifier_name
            n_args = 0

            self.eat(self.tokenizer.current_token_str)
            if self.tokenizer.current_token_str == "[":  # array
                self.eat("[")
                self.compile_expression()
                self.vmwriter.write_push(JACK_KINDS_TO_VM_SEGMENTS[identifier_kind], identifier_index)
                self.vmwriter.write_arithmetic(COMMAND_ADD)  # adding the index of the array to the starting address
                self.vmwriter.write_pop(VM_SEGMENT_POINTER, 1)
                self.vmwriter.write_push(VM_SEGMENT_THAT,0)
                self.eat("]")

            elif self.tokenizer.current_token_str == ".":  # subroutine_call-class/var name
                # todo - the code is duplicate - can move it to a function
                if identifier_kind is not None:  # var (object) name, push it as argument
                    self.vmwriter.write_push(JACK_KINDS_TO_VM_SEGMENTS[identifier_kind],
                                             identifier_index)  
                    n_args += 1
                callee_name = callee_name + self.tokenizer.current_token_str
                self.eat('.')
                # concat the method name to the class/empty callee name
                callee_name = callee_name + self.tokenizer.current_token_str
                self.eat(self.tokenizer.current_token_str)  # method name
                self.eat("(")
                n_args = self.compile_expression_list(n_args)
                self.eat(")")
                self.vmwriter.write_call(callee_name, n_args)
                # the returned value will be poped by the compile_do or compile_let
            elif self.tokenizer.current_token_str == "(":  # subroutine_call-
                # todo - the code is duplicate - can move it to a function
                self.eat("(")
                n_args = self.compile_expression_list(n_args)
                self.eat(")")
                callee_name = self.class_name + "." +  identifier_name
                self.vmwriter.write_call(callee_name, n_args)
                # the returned value will be poped by the compile_do or compile_let
            else:  # var_name, push it
                var_kind = self.symbols.kind_of(var_name)
                var_index = self.symbols.index_of(var_name)
                self.vmwriter.write_push(JACK_KINDS_TO_VM_SEGMENTS[var_kind], var_index)
        self.print_xml_header("/term", -1)
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.vmwriter.write_jack_command_header(" compile_do/call ", 1)
        self.print_xml_header("doStatement", 1)
        self.eat("do")
        self.print_xml_var_info(self.tokenizer.current_token_str)

        # collect information for the case of object or class call
        identifier_name = self.tokenizer.current_token_str
        identifier_kind = self.symbols.kind_of(identifier_name)

        if identifier_kind is not None:  # known object
            identifier_type = self.symbols.type_of(identifier_name)
            identifier_index = self.symbols.index_of(identifier_name)
            callee_name = identifier_type
        else:  # unknown class
            callee_name =  identifier_name
        n_args = 0
        self.eat(self.tokenizer.current_token_str)  # class/variable/subroutine name

        if self.tokenizer.current_token_str == '.':
            if identifier_kind is not None:  # var (object) name, push it as argument
                self.vmwriter.write_push(JACK_KINDS_TO_VM_SEGMENTS[identifier_kind],
                                         identifier_index)  
                n_args += 1
            callee_name = callee_name + "."
            self.eat('.')
            # concat the method name to the class/empty callee name
            callee_name = callee_name + self.tokenizer.current_token_str
            self.eat(self.tokenizer.current_token_str)  # method name
            self.eat("(")
            n_args = self.compile_expression_list(n_args)
            self.eat(")")
            #  self.eat(";")
            self.vmwriter.write_call(callee_name, n_args)  
        else:                                #  funciton name
            self.vmwriter.write_push(VM_SEGMENT_POINTER, 0)
            n_args = 1
            self.eat("(")
            n_args = self.compile_expression_list(n_args)
            self.eat(")")
            callee_name = self.class_name + "." + identifier_name
            self.vmwriter.write_call(callee_name, n_args)  
        self.eat(";")

        self.vmwriter.write_pop(VM_SEGMENT_TEMP, 0)
        self.print_xml_header("/doStatement", -1)
        self.vmwriter.write_jack_command_header("", -1)  

    def compile_expression_list(self, num_args: int) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        # num_args = 0
        self.print_xml_header("expressionList", 1)
        if self.tokenizer.current_token_str != ")":
            # first expression
            self.compile_expression()
            num_args += 1
            #  no need to push the argument, it was done by compile_expression
            # more expressions
            while self.tokenizer.has_more_tokens():
                if self.tokenizer.current_token_str == ',':
                    self.eat(",")
                    self.compile_expression()  # next expression
                    num_args += 1
                    #  no need to push the argument, it was done by compile_expression
                else:
                    break
        return num_args
        self.print_xml_header("/expressionList", -1)

    #  from here it is old code that should be deleted

    def get_token_value_str(self) -> str:
        token_type = self.tokenizer.token_type()
        if token_type == T_KEYWORD:
            return self.tokenizer.keyword()
        if token_type == T_SYMBOL:
            return self.tokenizer.symbol()
        if token_type == T_IDENTIFIER:
            return self.tokenizer.identifier()
        # todo - handle the 'problem'
        if token_type == T_INT_CONST:
            return self.tokenizer.int_val()
        if token_type == T_STRING_CONST:
            return self.tokenizer.string_val()
        return ""

    def print_xml_eat(self, expected_token: str) -> None:
        if expected_token != self.tokenizer.current_token_str:
            # error case
            return
        token_type_str = TOKEN_TYPES_STRINGS[self.tokenizer.token_type()]
        # token_value_str = self.TOKEN_VALUE_STRINGS[self.tokenizer.token_type()]
        token_value_str = self.get_token_value_str()
        for i in range(self.num_of_tabs):
            self.output_stream.write("  ")
        self.output_stream.write("<" +
                                 token_type_str +
                                 "> " +
                                 token_value_str +
                                 " </" +
                                 token_type_str +
                                 ">" + "\n")
        # not needed any more if self.tokenizer.has_more_tokens():
        # not needed any more    self.tokenizer.advance()

    def print_xml_class_subroutine_info(self,
                                        name: str,
                                        var_type: str,
                                        kind: str) -> None:
        return  # xml
        self.output_stream.write("=JUST PRINT name=" +
                                 name +
                                 "   =type=" +
                                 var_type +
                                 "   =kind=" +
                                 kind +
                                 "=====" +
                                 "\n")

    def print_xml_var_info(self,
                           name: str) -> None:
        return  # xml
        kind = self.symbols.kind_of(name)
        if kind != None:
            var_type = self.symbols.type_of(name)
            index_int = self.symbols.index_of(name)
            index = str(index_int)
            self.output_stream.write("=LOOK FOR name=" +
                                     name +
                                     "   =type=" +
                                     var_type +
                                     "   =kind=" +
                                     kind +
                                     "   =index=" +
                                     index +
                                     "\n")
        else:
            self.output_stream.write("=name=" +
                                     name +
                                     "  was not found" +
                                     "\n")

    def print_xml_table_entry(self, name: str, new_symbol: bool) -> None:
        return  # xml

        var_type = self.symbols.type_of(name)
        if var_type == None:
            return
        kind = self.symbols.kind_of(name)
        if kind == None:
            return
        index_int = self.symbols.index_of(name)
        index = str(index_int)
        self.output_stream.write("=name=" +
                                 name +
                                 "   =type=" +
                                 var_type +
                                 "   =kind=" +
                                 kind +
                                 "   =index=" +
                                 index +
                                 "  =is_new=" +
                                 str(new_symbol) +
                                 "\n")


    def print_xml_header(self, header: str, shift: int):
        return  # xml
        if header != "":
            if shift < 0:
                self.num_of_tabs -= 1
            for i in range(self.num_of_tabs):
                self.output_stream.write("  ")
            self.output_stream.write("<" +
                                     header +
                                     ">" + "\n")
            if shift > 0:
                self.num_of_tabs += 1



