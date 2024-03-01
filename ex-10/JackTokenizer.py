"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


SLASH = '/'
ASTERISK = '*'
SPACE = ' '

FIRST_CHAR = 0
FIRST_TOKEN = ""
QUOTA = '"'


# token types
T_KEYWORD = "KEYWORD"
T_SYMBOL = "SYMBOL"
T_IDENTIFIER = "IDENTIFIER"
T_INT_CONST = "INT_CONST"
T_STRING_CONST = "STRING_CONST"
T_ILLEGAL = "ILLEGAL_TOKEN"

NO_STRING_NO_COMMENT = 0
IN_STRING = 1
NO_COMMENT = 2        # current char is not part of any comment
START_COMMENT = 3     # status was NO_COMMENT, and  current char is '/'
IN_COMMENT_TYPE1 = 4  # state was "START_COMMENT" and current char is '/'
IN_COMMENT_TYPE2 = 5  # state was "START_COMMENT" and current char is '*'
END_COMMENT = 6       # state was "IN_COMMENT_TYPE2" and current char is '*'




KEYWORDS_SET = {'class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                'false', 'null', 'this', 'let', 'do', 'if', 'else',
                'while', 'return'}

SYMBOLS_SET = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
               '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#'}


def _is_whitespace(line):
    """
    end_white = 0
    for n in range(len(line), 0, -1):
        if line[n].isspace():
            end_white += 1
    """

    if line == "" or line.isspace():
        return True
    return False


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        self.input_lines_arr = input_stream.read().splitlines()  # Array of file lines
        self.input_lines_arr_no_empty = []
        self.stripped_lines_arr = []
        self.current_token_str = ""
        self.current_char_index = FIRST_CHAR
        self.current_line = 0
        self.cur_char_in_line = 0
        self.total_len = 0

        self.strip_all_line()
        if len(self.stripped_lines_arr) == 0:
            pass
        line = self.stripped_lines_arr[0]
        self.skip_spaces_in_line(line)
        if self.has_more_tokens():
            self.advance()

    def skip_spaces_in_line(self, line):
        for char in line:
            if char.isspace():
                self.cur_char_in_line += 1
                self.current_char_index += 1
            else:
                break

    def strip_all_line(self):

        for i in range(len(self.input_lines_arr)):
            line = self.input_lines_arr[i]
            if not _is_whitespace(line):
                self.input_lines_arr_no_empty.append(line)


        state = NO_STRING_NO_COMMENT
        strip_line = ""
        char_index = 0
        start_comment2_index = 0
        for i in range(len(self.input_lines_arr_no_empty)):
            line = self.input_lines_arr_no_empty[i]
            for char in line:
                char_index += 1
                if state == NO_STRING_NO_COMMENT:
                    if char == '"':
                        strip_line = strip_line + char
                        self.total_len += 1
                        state = IN_STRING
                    elif char == SLASH:
                        state = START_COMMENT
                    else:
                        strip_line = strip_line + char
                        self.total_len += 1
                elif state == IN_STRING:
                    strip_line = strip_line + char
                    self.total_len += 1
                    if char == '"':
                        state = NO_STRING_NO_COMMENT
                elif state == START_COMMENT:
                    if char == SLASH:
                        state = IN_COMMENT_TYPE1
                    elif char == ASTERISK:
                        state = IN_COMMENT_TYPE2
                        start_comment2_index = char_index
                    else:
                        strip_line = strip_line + SLASH
                        self.total_len += 1
                        strip_line = strip_line + char
                        self.total_len += 1
                        state = NO_STRING_NO_COMMENT
                elif state == IN_COMMENT_TYPE1:
                    pass
                elif state == IN_COMMENT_TYPE2:
                    if char == ASTERISK:
                        #if (start_comment2_index + 1) == char_index:
                        #    pass
                        #else:
                        state = END_COMMENT
                elif state == END_COMMENT:
                    if char == SLASH:
                        state = NO_STRING_NO_COMMENT
                    elif char == ASTERISK:
                        pass
                    else:
                        state = IN_COMMENT_TYPE2

            if state == IN_COMMENT_TYPE1:
                state = NO_STRING_NO_COMMENT
            elif state == END_COMMENT:
                state = IN_COMMENT_TYPE2

            if not _is_whitespace(strip_line):
                self.stripped_lines_arr.append(strip_line)
                strip_line = ""

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        if self.current_char_index < self.total_len:
            return True
        return False

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        # start from the current char at the current line
        line = self.stripped_lines_arr[self.current_line]
        self.current_token_str = ""

        # in case the token is just the last char at the line
        if self.cur_char_in_line == len(line) - 1:
            self.current_token_str += line[self.cur_char_in_line]
            self.current_char_index += 1
            self.advance_to_next_line()
            return

        # in case the char is a symbol
        if line[self.cur_char_in_line] in SYMBOLS_SET:
            self.advance_symbol(line)
            return

        # in case the char is a string
        if line[self.cur_char_in_line] == QUOTA:
            self.advance_quota(line)
            return

        b_found_whitespace = False
        #  add the current char to the token and move to the next char
        self.current_token_str += line[self.cur_char_in_line]
        self.cur_char_in_line += 1
        self.current_char_index += 1

        # continue adding chars to the token until whitespace or new symbol
        for char in line[self.cur_char_in_line:]:
            # in case a whitespace was found, skip all whitespaces at the line
            if b_found_whitespace is True:
                if char.isspace():
                    self.cur_char_in_line += 1
                    self.current_char_index += 1
                    continue
                else:
                    return
            else:
                if line[self.cur_char_in_line] == '.':
                    pass
                # symbol was found: that means end of token was reached
                if char in SYMBOLS_SET:
                    return
                # whitespace was found:  means end of token was reached
                #          yet to skip the rest of whitespaces at the line
                if char.isspace():
                    b_found_whitespace = True
                    self.cur_char_in_line += 1
                    self.current_char_index += 1
                # continue add chars to the current token
                else:
                    self.current_token_str += char
                    self.cur_char_in_line += 1
                    self.current_char_index += 1
        # at this point the char was the last one at the line
        # so moving to the next line
        self.advance_to_next_line()

    def advance_quota(self, line):
        b_in_quota = True
        self.current_token_str += line[self.cur_char_in_line]
        self.cur_char_in_line += 1
        self.current_char_index += 1
        for char in line[self.cur_char_in_line:]:
            if b_in_quota is True:
                self.current_token_str += line[self.cur_char_in_line]
                self.cur_char_in_line += 1
                self.current_char_index += 1
            else:
                if char.isspace():
                    self.cur_char_in_line += 1
                    self.current_char_index += 1
                else:
                    return
            if char == QUOTA:
                b_in_quota = False
        # in case all chars were read from the line - move to the next one
        if self.cur_char_in_line == len(line):
            self.current_line += 1
            if self.current_line < len(self.stripped_lines_arr):
                # skip whitespaces at the line
                line = self.stripped_lines_arr[self.current_line]
                self.cur_char_in_line = 0
                self.skip_spaces_in_line(line)
        return

    def advance_symbol(self, line):
        self.current_token_str += line[self.cur_char_in_line]
        self.cur_char_in_line += 1
        self.current_char_index += 1
        start_index = self.cur_char_in_line
        for char in line[start_index:]:
            if char.isspace():
                self.current_char_index += 1
                self.cur_char_in_line += 1
            else:
                return
        # at this point the symbol was the last char at previous line
        # so moving to the next line
        self.advance_to_next_line()
        return

    def advance_to_next_line(self):
        self.current_line += 1
        if self.current_line < len(self.stripped_lines_arr):
            # skip whitespaces at the line
            line = self.stripped_lines_arr[self.current_line]
            self.cur_char_in_line = 0
            self.skip_spaces_in_line(line)

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.current_token_str in KEYWORDS_SET:
            return T_KEYWORD
        elif self.current_token_str in SYMBOLS_SET:
            return T_SYMBOL
        elif self.current_token_str[0] == QUOTA:
            return T_STRING_CONST
        elif self.current_token_str.isdigit():
            return T_INT_CONST
        else:
            return T_IDENTIFIER

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        return self.current_token_str

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if self.current_token_str == '<':
            return "&lt;"
        if self.current_token_str == '>':
            return "&gt;"
        if self.current_token_str == '&':
            return "&amp;"
        if self.current_token_str == '"':
            return "&quot;"
        else:
            return self.current_token_str

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        return self.current_token_str

    # todo - should the function return int or str??
    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        return self.current_token_str

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        return self.current_token_str[1:-1]

    def token_val(self) -> str:
        return self.current_token_str
