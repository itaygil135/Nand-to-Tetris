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
# T_KEYWORD = "KEYWORD"
# T_SYMBOL = "SYMBOL"
# T_IDENTIFIER = "IDENTIFIER"
# T_INT_CONST = "INT_CONST"
# T_STRING_CONST = "STRING_CONST"

# kinds names
#FIELD_KIND_STR = "field"
#STATIC_KIND_STR = "static"
#ARG_KIND_STR = "argument"
#LOCAL_KIND_STR = "local"

FIELD_KIND = "FIELD"
STATIC_KIND = "STATIC"
ARG_KIND = "ARG"
VAR_KIND = "VAR"

# kinds used by class
CLASS_VAR_KINDS = {FIELD_KIND, STATIC_KIND}

#kinds used by subroutine
SUBROUTINE_VAR_KINDS = {ARG_KIND,VAR_KIND}

# kinds that has list of element, getting to each using index
INDEXED_KINDS_SET = {FIELD_KIND,
                    STATIC_KIND,
                    ARG_KIND,
                    VAR_KIND}


class SymbolEntry :
    def __init__(self, arg_name:str , arg_type: str, arg_kind: str, arg_index:int) -> None:
        self.name = arg_name
        self.type = arg_type
        self.kind = arg_kind
        self.symbol_index = arg_index



class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!

        # dictionary of SymbolEntry objects, using the name as key
        self.class_table = {}
        self.subroutine_table = {}

        self.output_stream = ""


        self.kinds_index = { FIELD_KIND: 0,
                           STATIC_KIND: 0,
                           ARG_KIND: 0,
                           VAR_KIND:0}

        self.tokenizer_api = JackTokenizer

        # self.TOKEN_VALUE_STRINGS = {T_KEYWORD: self.tokenizer_api.keyword,
        #                             T_SYMBOL: self.tokenizer_api.symbol,
        #                             T_IDENTIFIER: self.tokenizer_api.identifier,
        #                             T_INT_CONST: self.tokenizer_api.int_val,
        #                             T_STRING_CONST: self.tokenizer_api.string_val}



    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        # self.subroutine_kind = {}
        self.subroutine_table = {}
        self.kinds_index[ARG_KIND] = 0
        self.kinds_index[VAR_KIND] = 0
        pass

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!
        index = self.kinds_index[kind]
        if kind in CLASS_VAR_KINDS:
            table_name = "CLASS"
            self.class_table[name] = SymbolEntry(name, type, kind, self.kinds_index[kind])
            self.kinds_index[kind] += 1

        elif kind in SUBROUTINE_VAR_KINDS:
            table_name = "SUBROUTINE"
            self.subroutine_table[name] = SymbolEntry(name, type, kind, self.kinds_index[kind])
            self.kinds_index[kind] += 1

        else:
            pass  # keep this line for debugging error case

        self.write_symbol_comment(table_name, kind, type, name, index)



    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        if kind in INDEXED_KINDS_SET:
            return self.kinds_index[kind]
        else:
            return 0  # keep this line for debugging error case

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        if name in self.subroutine_table:
            return self.subroutine_table[name].kind
        elif name in self.class_table:
            return self.class_table[name].kind
        else:
            return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        if name in self.subroutine_table:
            return self.subroutine_table[name].type
        elif name in self.class_table:
            return self.class_table[name].type
        else:
            return None  # keep this line for debugging error case

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        if name in self.subroutine_table:
            return self.subroutine_table[name].symbol_index
        elif name in self.class_table:
            return self.class_table[name].symbol_index
        else:
            return -1  # keep this line for debugging error case

    def set_output_stream(self, output_stream: str) -> None:
        self.output_stream = output_stream

    def write_symbol_comment(self, table:str, kind: str, type: str, name: str , index:int) -> None:
        if table is not str:
            pass
        if kind is not str:
            pass
        if type is not str:
            pass
        if name is not str:
            pass
        """
        self.output_stream.write("//  define  " +
                                 table + "  " +
                                 kind + " " +
                                 type + "  " +
                                 name + "  " +
                                 str(index) + "\n")
                                 """
