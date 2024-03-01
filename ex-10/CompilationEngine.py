"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

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

CLASS_VAR_DEC_SET = {'static', 'field'}
SUBRUTINE_DEC_SET = {'constructor', 'function', 'method'}
OP_SET = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
UNARY_OP_SET = {"-", "~", "^", "#"}
KEYWORD_CONSTANT_SET = {"true", "false", "null", "this"}


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

        self.num_of_tabs = 0

        # todo - try to use this dic
        self.TOKEN_VALUE_STRINGS = {T_KEYWORD: self.tokenizer.keyword,
                                    T_SYMBOL: self.tokenizer.symbol,
                                    T_IDENTIFIER: self.tokenizer.identifier,
                                    T_INT_CONST: self.tokenizer.int_val,
                                    T_STRING_CONST: self.tokenizer.string_val}

        self.var_types_set = {"int", "char", "boolean"}
        self.compile_class()

    def write_header(self, header: str, shift: int):
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

    def eat(self, expected_token: str) -> None:
        if expected_token != self.tokenizer.current_token_str:
            # error case
            return
        token_str = TOKEN_TYPES_STRINGS[self.tokenizer.token_type()]
        # token_value_str = self.TOKEN_VALUE_STRINGS[self.tokenizer.token_type()]
        token_value_str = self.get_token_value_str()
        for i in range(self.num_of_tabs):
            self.output_stream.write("  ")
        self.output_stream.write("<" +
                                 token_str +
                                 "> " +
                                 token_value_str +
                                 " </" +
                                 token_str +
                                 ">" + "\n")
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.write_header("class", 1)
        self.eat("class")
        self.eat(self.tokenizer.current_token_str)               # class name
        self.eat("{")
        # add the class name to the set of variables types
        # self.var_types_set.add(self.tokenizer.current_token_str)

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in CLASS_VAR_DEC_SET:
                self.compile_class_var_dec()
            else:
                break

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in SUBRUTINE_DEC_SET:
                self.compile_subroutine()
            else:
                break

        self.eat("}")
        self.write_header("/class", -1)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.compile_variables_declaration("classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.write_header("subroutineDec", 1)
        self.eat(self.tokenizer.current_token_str)  # constructor / function / method
        self.eat(self.tokenizer.current_token_str)  # void / type
        self.eat(self.tokenizer.current_token_str)  # subroutine name
        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.write_header("subroutineBody", 1)
        self.eat("{")

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == 'var':
                self.compile_var_dec()
            else:
                break

        self.compile_statements()
        self.eat("}")
        self.write_header("/subroutineBody", -1)
        self.write_header("/subroutineDec", -1)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!

        self.write_header("parameterList", 1)
        if self.tokenizer.current_token_str == ')':
            self.write_header("/parameterList", -1)
            return
        self.eat(self.tokenizer.current_token_str)  # parameter type
        self.eat(self.tokenizer.current_token_str)  # parameter name

        # more parameters
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str == ',':
                self.eat(',')
                self.eat(self.tokenizer.current_token_str)  # parameter type
                self.eat(self.tokenizer.current_token_str)  # parameter name
            else:
                break

        self.write_header("/parameterList", -1)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        # todo - how should new type be handled ???

        self.compile_variables_declaration("varDec")

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

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.write_header("statements", 1)
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
                self.write_header("/statements", -1)
                return

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.write_header("doStatement", 1)
        self.eat("do")

        self.eat(self.tokenizer.current_token_str)  # class/variable/subroutine name
        if self.tokenizer.current_token_str == '.':
            self.eat(".")
            self.eat(self.tokenizer.current_token_str)  # method name
        self.eat("(")
        self.compile_expression_list()
        self.eat(")")

        self.eat(";")
        self.write_header("/doStatement", -1)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.write_header("letStatement", 1)
        self.eat("let")
        self.eat(self.tokenizer.current_token_str)
        if self.tokenizer.current_token_str == "[":
            self.eat("[")
            self.compile_expression()
            self.eat("]")
        self.eat("=")
        self.compile_expression()
        self.eat(";")
        self.write_header("/letStatement", -1)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.write_header("whileStatement", 1)
        self.eat("while")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.write_header("/whileStatement", -1)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.write_header("returnStatement", 1)
        self.eat("return")
        if self.tokenizer.current_token_str != ';':
            self.compile_expression()
        self.eat(";")
        self.write_header("/returnStatement", -1)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.write_header("ifStatement", 1)
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        if self.tokenizer.current_token_str == "else":
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
        self.write_header("/ifStatement", -1)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!

        self.write_header("expression", 1)
        # first term
        self.compile_term()
        # more terms
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token_str in OP_SET:
                self.eat(self.tokenizer.current_token_str)  # op
                self.compile_term()  # next term
            else:
                break
        self.write_header("/expression", -1)

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
        self.write_header("term", 1)
        if self.tokenizer.token_type() == T_INT_CONST   \
                or self.tokenizer.token_type() == T_STRING_CONST \
                or self.tokenizer.token_type() == KEYWORD_CONSTANT_SET:
            self.eat(self.tokenizer.current_token_str)
        elif self.tokenizer.current_token_str in UNARY_OP_SET:
            self.eat(self.tokenizer.current_token_str)
            self.compile_term()
        elif self.tokenizer.current_token_str == "(":
            self.eat("(")
            self.compile_expression()
            self.eat(")")
        else:
            # eat var_name | var_name[] | subroutine_call
            self.eat(self.tokenizer.current_token_str)
            if self.tokenizer.current_token_str == "[":  # array
                self.eat("[")
                self.compile_expression()
                self.eat("]")
            elif self.tokenizer.current_token_str == ".":  # subroutine_call-class/var name
                self.eat('.')
                self.eat(self.tokenizer.current_token_str)  # method name
                self.eat("(")
                self.compile_expression_list()
                self.eat(")")
            elif self.tokenizer.current_token_str == "(":  # subroutine_call-subroutine_name
                self.eat("(")
                self.compile_expression_list()
                self.eat(")")
            else:  # var_name, nothing to do
                pass

        self.write_header("/term", -1)
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!

        self.write_header("expressionList", 1)
        if self.tokenizer.current_token_str != ")":
            # first expression
            self.compile_expression()
            # more expressions
            while self.tokenizer.has_more_tokens():
                if self.tokenizer.current_token_str == ',':
                    self.eat(",")
                    self.compile_expression()  # next expression
                else:
                    break
        self.write_header("/expressionList", -1)
