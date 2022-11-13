import os
from pprint import pprint as print
from typing import Any

from tokenizer import Token, TokenKind, Tokenizer

TOKENS = {
    TokenKind.OPEN_PAREN: "(",
    TokenKind.CLOSE_PAREN: ")",
    TokenKind.OPEN_CURLY: "{",
    TokenKind.CLOSE_CURLY: "}",
    TokenKind.OPEN_SQUARE: "[",
    TokenKind.CLOSE_SQUARE: "]",
    TokenKind.SEMICOLON: ";",
    TokenKind.COMMA: ",",
    TokenKind.LINE_COMMENT: '//',
    TokenKind.EQUIV: "===",
    TokenKind.NEQUIV: "!==",
    TokenKind.EQ: "==",
    TokenKind.NEQ: "!=",
    TokenKind.PLUS_ASSIGNMENT: "+=",
    TokenKind.MINUS_ASSIGNMENT: "-=",
    TokenKind.MUL_ASSIGNMENT: "*=",
    TokenKind.DIV_ASSIGNMENT: "/=",
    TokenKind.ASSIGNMENT: "=",
    TokenKind.GE: ">=",
    TokenKind.LE: "<=",
    TokenKind.INCR: "++",
    TokenKind.DECR: "--",
    TokenKind.GT: ">",
    TokenKind.LT: "<",
    TokenKind.PLUS: "+",
    TokenKind.MINUS: "-",
    TokenKind.MUL: "*",
    TokenKind.DIV: "/",
    TokenKind.MOD: "%",
    TokenKind.AND: "&&",
    TokenKind.OR: "||",
}

KEYWORDS = [
    "break", "const", "case", "catch", "continue", "default",
    "delete", "else", "false", "finally", "for", "function",
    "if", "let", "null", "return", "switch", "throw", "try",
    "true", "var", "while", "do"
]


class JSParser:

    def parse_string(self, string: str) -> dict[str, Any]:
        self.tokenizer = Tokenizer.from_string(string, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program()

    def parse_file(self, file_path: str) -> dict[str, Any]:
        self.tokenizer = Tokenizer.from_file(file_path, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program()

    def __program(self) -> dict[str, Any]:
        node: dict[Any, Any] = {"type": "Program"}
        if self.lookahead is not None:
            node["body"] = self.__statement_list()
        else:
            node["body"] = []
        return node

    def __statement_list(self, until: TokenKind | None = None) -> list[dict[str, Any]]:
        statements = [self.__statement()]

        assert self.lookahead is not None

        while not self.tokenizer.stop and self.lookahead.kind != until:
            statements.append(self.__statement())

        return statements

    def __statement(self) -> dict[str, Any]:

        assert self.lookahead is not None

        if self.is_keyword(self.lookahead):
            match self.lookahead.text:
                case "while": return self.__while_statement()
                case "do": return self.__dowhile_statement()
                case "if": return self.__if_statement()
                case _: ...

        match self.lookahead.kind:
            case TokenKind.OPEN_CURLY:
                return self.__block_statement()
            case TokenKind.SEMICOLON:
                return self.__empty_statement()
            case _:
                return self.__expression_statement()

    def __empty_statement(self) -> dict[str, Any]:
        self.__consume_token(TokenKind.SEMICOLON)
        return {"type": "EmptyStatement"}

    def __block_statement(self) -> dict[str, Any]:
        self.__consume_token(TokenKind.OPEN_CURLY)

        assert self.lookahead is not None

        node = {
            "type": "BlockStatement",
            "body": self.__statement_list(TokenKind.CLOSE_CURLY)
                    if self.lookahead.kind != TokenKind.CLOSE_CURLY
                    else []
        }
        self.__consume_token(TokenKind.CLOSE_CURLY)

        return node

    def __while_statement(self) -> dict[str, Any]:
        self.__consume_keyword("while")
        self.__consume_token(TokenKind.OPEN_PAREN)
        condition = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        body = self.__statement()

        return {
            "type": "WhileStatement",
            "condition": condition,
            "body": body
        }

    def __if_statement(self) -> dict[str, Any]:
        node: dict[str, Any] = {"type": "IfStatement"}
        self.__consume_keyword("if")
        self.__consume_token(TokenKind.OPEN_PAREN)
        node["condition"] = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        node["body"] = self.__statement()

        assert self.lookahead is not None

        if self.is_keyword(self.lookahead):
            if self.lookahead.text == "else":
                self.__consume_keyword("else")
                node["alternative"] = self.__statement()

        return node

    def __dowhile_statement(self) -> dict[str, Any]:
        self.__consume_keyword("do")
        body = self.__statement()
        self.__consume_keyword("while")
        self.__consume_token(TokenKind.OPEN_PAREN)
        condition = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)

        assert self.lookahead is not None

        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)

        return {
            "type": "DoWhileStatement",
            "body": body,
            "condition": condition
        }

    def __expression_statement(self) -> dict[str, Any]:
        node = {"type": "ExpressionStatement", "body": self.__expression()}

        assert self.lookahead is not None

        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)

        return node

    def __expression(self) -> dict[str, Any]:
        return self.__assignment_expr()

    def __assignment_expr(self) -> dict[str, Any]:
        left_token = self.lookahead
        node = self.__logic_expr()
        ops = [
            TokenKind.ASSIGNMENT, TokenKind.PLUS_ASSIGNMENT,
            TokenKind.MINUS_ASSIGNMENT, TokenKind.MUL_ASSIGNMENT,
            TokenKind.DIV_ASSIGNMENT
        ]

        assert self.lookahead is not None

        if self.lookahead.kind in ops:
            if node["type"] != "Identifier":
                self.tokenizer.print_err("Invalid left-hand side", left_token)
            node = {
                "type": "AssignmentExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__expression()
            }
        return node

    def __logic_expr(self) -> dict[str, Any]:
        return self.__or_expr()

    def __or_expr(self) -> dict[str, Any]:
        node = self.__and_expr()

        assert self.lookahead is not None

        while self.lookahead.kind == TokenKind.OR:
            node = {
                "type": "LogicalExpression",
                "operator": self.__consume_token(TokenKind.OR).text,
                "left": node,
                "right": self.__and_expr()
            }
        return node

    def __and_expr(self) -> dict[str, Any]:
        node = self.__binary_expr()

        assert self.lookahead is not None

        while self.lookahead.kind == TokenKind.AND:
            node = {
                "type": "LogicalExpression",
                "operator": self.__consume_token(TokenKind.AND).text,
                "left": node,
                "right": self.__binary_expr()
            }
        return node

    def __binary_expr(self) -> dict[str, Any]:
        return self.__comp_expr()

    def __comp_expr(self) -> dict[str, Any]:
        node = self.__add_expr()
        comp_ops = [
            TokenKind.EQUIV, TokenKind.NEQUIV,
            TokenKind.EQ, TokenKind.NEQ,
            TokenKind.GE, TokenKind.LE,
            TokenKind.GT, TokenKind.LT
        ]

        assert self.lookahead is not None

        while self.lookahead.kind in comp_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__add_expr()
            }
        return node

    def __add_expr(self) -> dict[str, Any]:
        node = self.__mul_expr()
        add_ops = [TokenKind.PLUS, TokenKind.MINUS]

        assert self.lookahead is not None

        while self.lookahead.kind in add_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__mul_expr()
            }
        return node

    def __mul_expr(self) -> dict[str, Any]:
        node = self.__prim_expr()
        mul_ops = [TokenKind.MUL, TokenKind.DIV]

        assert self.lookahead is not None

        while self.lookahead.kind in mul_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__prim_expr()
            }
        return node

    def __prim_expr(self) -> dict[str, Any]:
        node = {}

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.OPEN_PAREN:
                self.__consume_token(TokenKind.OPEN_PAREN)
                node = self.__expression()
                self.__consume_token(TokenKind.CLOSE_PAREN)
            case TokenKind.WORD:
                match self.lookahead.text:
                    case "true" | "false" | "null": node = self.__literal()
                    case _: node = self.__identifier()
            case _:
                node = self.__literal()
        return node

    def __identifier(self) -> dict[str, Any]:
        ident = self.__consume_token(TokenKind.WORD)
        if not self.is_keyword(ident):
            return {
                "type": "Identifier",
                "name": ident.text
            }
        else:
            self.tokenizer.print_err("unexpected use of keyword", ident)

    def __literal(self) -> dict[str, Any]:

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.NUMBER_LIT: return self.__numeric_literal()
            case TokenKind.STR_LIT: return self.__str_literal()
            case TokenKind.WORD:
                token = self.__consume_token(TokenKind.WORD)
                return {
                    "type": "Literal",
                    "value": None
                            if token.text == "null"
                            else True if token.text == "true"
                            else False,
                    "raw": token.text
                }
            case _:
                raise AssertionError("unreachable")

    def __numeric_literal(self) -> dict[str, Any]:
        token = self.__consume_token(TokenKind.NUMBER_LIT)
        return {"type": "Literal", "value": int(token.text), "raw": token.text}

    def __str_literal(self) -> dict[str, Any]:
        token = self.__consume_token(TokenKind.STR_LIT)
        assert len(token.text) >= 2, "unexpected string literal"
        value = token.text[1:-1]
        return {"type": "Literal", "value": value, "raw": token.text}

    def __consume_token(self, kind: TokenKind) -> Token:
        token = self.tokenizer.expect_token(kind)
        try:
            next_token = self.tokenizer.peek()
        except StopIteration:
            next_token = None
        if next_token is not None:
            self.lookahead = next_token
        return token

    def __consume_keyword(self, name: str) -> Token:
        token = self.tokenizer.expect_keyword(name)
        try:
            next_token = self.tokenizer.peek()
        except StopIteration:
            next_token = None
        if next_token is not None:
            self.lookahead = next_token
        return token

    def is_keyword(self, token: Token) -> bool:
        return token.text in KEYWORDS


parser = JSParser()

print(parser.parse_file(os.path.dirname(os.path.abspath(__file__)) + "/test/simple.js"))

# for token in (tokenizer := Tokenizer.from_file("test/inputAcc.js", TOKENS)):
#     if token.kind == TokenKind.WORD and token.text == "if":
#         func_name = tokenizer.expect_token(TokenKind.OPEN_PAREN)
