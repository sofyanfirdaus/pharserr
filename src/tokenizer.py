from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto
import sys


class TokenKind(Enum):
    """ Some generic tokens enumeration """
    WORD = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_CURLY = auto()
    CLOSE_CURLY = auto()
    OPEN_SQUARE = auto()
    CLOSE_SQUARE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    STR_LIT = auto()
    NUMBER_LIT = auto()
    EQUIV = auto()
    NEQUIV = auto()
    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    ASSIGNMENT = auto()
    PLUS_ASSIGNMENT = auto()
    MINUS_ASSIGNMENT = auto()
    MUL_ASSIGNMENT = auto()
    DIV_ASSIGNMENT = auto()
    MOD_ASSIGNMENT = auto()
    INCR = auto()
    DECR = auto()
    AND = auto()
    OR = auto()
    COLON = auto()
    QUESTION_MARK = auto()
    LINE_COMMENT = auto()


@dataclass
class Location:
    row: int
    col: int
    file_path: str

    def __str__(self) -> str:
        return f"{self.file_path}:{self.row}:{self.col}"

    def __format__(self, format_spec: str) -> str:
        return f"{self.__str__():{format_spec}}"


@dataclass
class Token:
    text: str
    kind: TokenKind
    location: Location


class Tokenizer(Iterator[Token]):

    def __init__(self, content: str, file_path: str,
                 token_pairs: dict[TokenKind, str]) -> None:
        self.content = content
        self.file_path = file_path
        self.line = ""
        self.full_line = ""
        self.row = 0
        self.token_pairs = token_pairs
        self.stop = False

        self.peek_token: Token | None = None

    @classmethod
    def from_string(cls, string: str, token_pairs: dict[TokenKind, str]):
        return cls(string, "string", token_pairs)

    @classmethod
    def from_file(cls, file_path: str, token_pairs: dict[TokenKind, str]):
        with open(file_path, 'r') as file:
            content = "".join(file.readlines())
        return cls(content, file_path, token_pairs)

    def location(self) -> Location:
        return Location(self.row,
                        len(self.full_line) - len(self.line) + 1,
                        self.file_path)

    def __next_line(self) -> None:
        nl = self.content.find('\n')
        if nl == -1:
            self.full_line = self.content
            self.content = ""
        else:
            self.full_line = self.content[:nl]
            self.content = self.content[nl + 1:]
        self.row += 1
        self.line = self.full_line.lstrip()

    def __iter__(self) -> Iterator[Token]:
        return self

    def expect_token(self, kind: TokenKind, err_msg: str = ""):
        try:
            token = next(self)
            if token.kind != kind:
                if err_msg:
                    self.print_err(
                        f"Expected {err_msg}, but got `{token.text}`", token)
                else:
                    self.print_err(
                        f"Expected `{self.token_pairs[kind]}`, but got `{token.text}`",
                        token)
            return token
        except StopIteration:
            self.print_err(
                f"Expected `{self.token_pairs[kind]}`, but got nothing")

    def expect_keyword(self, name: str):
        token = self.expect_token(TokenKind.WORD, "keyword")
        if token.text != name:
            self.print_err(f"Expected keyword `{name}`", token)
        return token

    def __next__(self) -> Token:
        token = self.peek()
        self.peek_token = None
        if token is not None:
            return token
        else:
            raise StopIteration()

    def print_err(self, err_msg: str, token: Token | None = None, full_line: str | None = None):
        if token is not None:
            length = len(token.text)
            location = token.location
        else:
            length = 1
            location = self.location()
        if full_line is None:
            full_line = self.full_line
        print(f"{location}: ERROR: {err_msg}", file=sys.stderr)
        print("    |")
        print(f"{location.row:>4}| " + full_line)
        print("    | {0:>{1}}".format("^" * length, location.col + length - 1))
        raise SyntaxError(err_msg)

    def peek(self) -> Token | None:
        if self.peek_token is not None:
            return self.peek_token

        self.line = self.line.lstrip()

        while (len(self.line) == 0 and len(self.content) > 0) or \
                self.line.startswith(self.token_pairs[TokenKind.LINE_COMMENT]):
            self.__next_line()

        if len(self.line) == 0:
            self.stop = True
            return None

        location = self.location()

        for token_kind, token_text in self.token_pairs.items():
            if self.line.startswith(s := token_text):
                token = Token(s, token_kind, location)
                self.line = self.line[len(s):]
                self.peek_token = token
                return token

        if self.line[0].isalpha():
            end = next((i for i, c in enumerate(self.line)
                        if not (c.isalnum() or c == '_')), -1)
            if end != -1:
                s = self.line[:end]
                self.line = self.line[end:]
            else:
                s = self.line
                self.line = ""
            token = Token(s, TokenKind.WORD, location)
            self.peek_token = token
            return token
        elif self.line[0] in "0123456789.":
            gen = (i for i, c in enumerate(self.line) if not c.isdecimal())
            end = next(gen, -1)
            if self.line[end] == '.':
                end = next(gen, -1)
            if end != -1:
                s = self.line[:end]
                self.line = self.line[end:]
            else:
                s = self.line
                self.line = ""
            token = Token(s, TokenKind.NUMBER_LIT, location)
            self.peek_token = token
            return token
        elif (quote := self.line[0]) in "'\"`":
            end = self.line[1:].find(quote)
            if end == -1:
                self.print_err("Unterminated string literal")
            else:
                s = self.line[:end + 2]
                self.line = self.line[end + 2:]
                token = Token(s, TokenKind.STR_LIT, location)
                self.peek_token = token
                return token
        else:
            self.print_err(f"Unknown token starts with `{self.line[0]}`")
