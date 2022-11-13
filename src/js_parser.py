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
    TokenKind.DIV_ASSIGNMENT: "*=",
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
    TokenKind.AND: "&&",
    TokenKind.OR: "||",
}

KEYWORDS = [
    "break", "const", "case", "catch", "continue", "default",
    "delete", "else", "false", "finally", "for", "function",
    "if", "let", "null", "return", "switch", "throw", "try",
    "true", "var", "while"
]


class JSParser:

    def parse_string(self, string: str) -> dict:
        self.tokenizer = Tokenizer.from_string(string, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program()

    def parse_file(self, file_path: str) -> dict:
        self.tokenizer = Tokenizer.from_file(file_path, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program()

    def __program(self):
        node: dict[Any, Any] = {"type": "Program"}
        if self.lookahead is not None:
            node["body"] = self.__statement_list()
        else:
            node["body"] = []
        return node

    def __statement_list(self, until: TokenKind | None = None):
        statements = [self.__statement()]

        assert self.lookahead is not None

        while not self.tokenizer.stop and self.lookahead.kind != until:
            statements.append(self.__statement())

        return statements

    def __statement(self):

        assert self.lookahead is not None

        if self.is_keyword(self.lookahead):
            match self.lookahead.text:
                case "while": return self.__while_statement()

        match self.lookahead.kind:
            case TokenKind.OPEN_CURLY:
                return self.__block_statement()
            case TokenKind.SEMICOLON:
                return self.__empty_statement()
            case _:
                return self.__primary_expression()

    def __empty_statement(self):
        self.__consume_token(TokenKind.SEMICOLON)
        return {"type": "EmptyStatement"}

    def __block_statement(self):
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

    def __while_statement(self):
        self.__consume_token(TokenKind.WORD)
        self.__consume_token(TokenKind.OPEN_PAREN)
        condition = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        body = self.__statement()

        return {
            "type": "WhileStatement",
            "condition": condition,
            "body": body
        }

    def __primary_expression(self):
        node = {"type": "ExpressionStatement", "body": self.__expression()}
        ops = [
            TokenKind.ASSIGNMENT, TokenKind.PLUS_ASSIGNMENT,
            TokenKind.MINUS_ASSIGNMENT, TokenKind.MUL_ASSIGNMENT,
            TokenKind.DIV_ASSIGNMENT
        ]

        assert self.lookahead is not None

        if self.lookahead.kind in ops:
            node = {
                "type": "AssignmentStatement",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__expression()
            }
        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)
        return node

    def __expression(self):
        return self.__logic_expr()

    def __logic_expr(self):
        return self.__or_expr()

    def __or_expr(self):
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

    def __and_expr(self):
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

    def __binary_expr(self):
        return self.__comp_expr()

    def __comp_expr(self):
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

    def __add_expr(self):
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

    def __mul_expr(self):
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

    def __prim_expr(self):
        node = {}

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.OPEN_PAREN:
                self.__consume_token(TokenKind.OPEN_PAREN)
                node = self.__expression()
                self.__consume_token(TokenKind.CLOSE_PAREN)
            case TokenKind.WORD:
                match self.lookahead.text:
                    case "true" | "false": node = self.__literal()
                    case _: node = self.__identifier()
            case _:
                node = self.__literal()
        return node

    def __identifier(self):
        ident = self.__consume_token(TokenKind.WORD)
        if not self.is_keyword(ident):
            return {
                "type": "Identifier",
                "name": ident.text
            }
        else:
            self.tokenizer.print_err("unexpected use of keyword", ident)

    def __literal(self):

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.NUMBER_LIT: return self.__numeric_literal()
            case TokenKind.STR_LIT: return self.__str_literal()
            case TokenKind.WORD:
                token = self.__consume_token(TokenKind.WORD)
                return {
                    "type": "Literal",
                    "value": True if token.text == "true" else False,
                    "raw": token.text
                }

    def __numeric_literal(self):
        token = self.__consume_token(TokenKind.NUMBER_LIT)
        return {"type": "Literal", "value": int(token.text), "raw": token.text}

    def __str_literal(self):
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

    def is_keyword(self, token):
        return token.text in KEYWORDS


parser = JSParser()

print(parser.parse_file(os.path.dirname(os.path.abspath(__file__)) + "/test/simple.js"))

# for token in (tokenizer := Tokenizer.from_file("test/inputAcc.js", TOKENS)):
#     if token.kind == TokenKind.WORD and token.text == "if":
#         func_name = tokenizer.expect_token(TokenKind.OPEN_PAREN)
