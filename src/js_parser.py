import os
from pprint import pprint as print
from typing import Any

from tokenizer import Location, Token, TokenKind, Tokenizer

TOKENS = {
    TokenKind.OPEN_PAREN: "(",
    TokenKind.CLOSE_PAREN: ")",
    TokenKind.OPEN_CURLY: "{",
    TokenKind.CLOSE_CURLY: "}",
    TokenKind.OPEN_SQUARE: "[",
    TokenKind.CLOSE_SQUARE: "]",
    TokenKind.SEMICOLON: ";",
    TokenKind.COMMA: ",",
    TokenKind.LINE_COMMENT: "//",
    TokenKind.EQUIV: "===",
    TokenKind.NEQUIV: "!==",
    TokenKind.EQ: "==",
    TokenKind.NEQ: "!=",
    TokenKind.POW: "**",
    TokenKind.PLUS_ASSIGNMENT: "+=",
    TokenKind.MINUS_ASSIGNMENT: "-=",
    TokenKind.MUL_ASSIGNMENT: "*=",
    TokenKind.DIV_ASSIGNMENT: "/=",
    TokenKind.MOD_ASSIGNMENT: "%=",
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
    TokenKind.COLON: ":",
}

KEYWORDS = [
    "break",
    "const",
    "case",
    "catch",
    "continue",
    "default",
    "delete",
    "else",
    "false",
    "finally",
    "for",
    "function",
    "if",
    "let",
    "null",
    "return",
    "switch",
    "throw",
    "try",
    "true",
    "var",
    "while",
    "do",
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

    def __statement_list(self, until: list[TokenKind] = []) -> list[dict[str, Any]]:
        statements = [self.__statement()]

        assert self.lookahead is not None

        while not self.tokenizer.stop and self.lookahead.kind not in until:
            statements.append(self.__statement())

        return statements

    def __statement(self) -> dict[str, Any]:

        assert self.lookahead is not None

        if self.is_keyword(self.lookahead):
            match self.lookahead.text:
                case "while":
                    return self.__while_statement()
                case "do":
                    return self.__dowhile_statement()
                case "for":
                    return self.__for_statement()
                case "if":
                    return self.__if_statement()
                case "try":
                    return self.__try_statement()
                case "return":
                    return self.__return_statement()
                case "var" | "let" | "const":
                    return self.__variable_declaration()
                case "switch":
                    return self.__switch_statement()
                case _:
                    ...

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
            "body": self.__statement_list([TokenKind.CLOSE_CURLY])
            if self.lookahead.kind != TokenKind.CLOSE_CURLY
            else [],
        }
        self.__consume_token(TokenKind.CLOSE_CURLY)

        return node

    def __while_statement(self) -> dict[str, Any]:
        self.__consume_keyword("while")
        self.__consume_token(TokenKind.OPEN_PAREN)
        condition = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        body = self.__statement()

        return {"type": "WhileStatement", "condition": condition, "body": body}

    def __for_statement(self) -> dict[str, Any]:
        self.__consume_keyword("for")
        self.__consume_token(TokenKind.OPEN_PAREN)

        assert self.lookahead is not None

        init = test = update = None

        if self.is_keyword(self.lookahead):
            match self.lookahead.text:
                case "var" | "let" | "const":
                    init = self.__variable_declaration()
                case _:
                    ...
        else:
            if self.lookahead.kind != TokenKind.SEMICOLON:
                init = self.__expression()
            self.__consume_token(TokenKind.SEMICOLON)

        if self.lookahead.kind != TokenKind.SEMICOLON:
            test = self.__expression()
        self.__consume_token(TokenKind.SEMICOLON)

        if self.lookahead.kind != TokenKind.CLOSE_PAREN:
            update = self.__expression()

        self.__consume_token(TokenKind.CLOSE_PAREN)

        body = self.__statement()

        return {
            "type": "ForStatement",
            "init": init,
            "test": test,
            "update": update,
            "body": body,
        }

    def __if_statement(self) -> dict[str, Any]:
        self.__consume_keyword("if")
        self.__consume_token(TokenKind.OPEN_PAREN)
        condition = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        consequent = self.__statement()

        assert self.lookahead is not None

        alternative = None

        if self.is_keyword(self.lookahead):
            if self.lookahead.text == "else":
                self.__consume_keyword("else")
                alternative = self.__statement()

        return {
            "type": "IfStatement",
            "condition": condition,
            "consequent": consequent,
            "alternative": alternative,
        }

    def __switch_statement(self) -> dict[str, Any]:
        assert self.lookahead is not None

        self.__consume_keyword("switch")
        self.__consume_token(TokenKind.OPEN_PAREN)
        discriminant = self.__expression()
        self.__consume_token(TokenKind.CLOSE_PAREN)
        self.__consume_token(TokenKind.OPEN_CURLY)
        cases = []
        if self.lookahead.kind != TokenKind.CLOSE_CURLY:
            cases = self.__switchcase_list()
        self.__consume_token(TokenKind.CLOSE_CURLY)

        return {"type": "SwitchStatement", "discriminant": discriminant, "cases": cases}

    def __switchcase_list(self) -> list[dict[str, Any]]:
        switchcases = [self.__switchcase()]

        assert self.lookahead is not None

        while self.is_keyword(self.lookahead):
            if self.lookahead.text in ["case", "default"]:
                switchcases.append(self.__switchcase())

        return switchcases

    def __switchcase(self) -> dict[str, Any]:
        assert self.lookahead is not None

        test = None
        consequent = []

        stops = [TokenKind.WORD, TokenKind.CLOSE_CURLY]

        match self.lookahead.text:
            case "case":
                self.__consume_keyword("case")
                test = self.__expression()
                self.__consume_token(TokenKind.COLON)
                consequent = self.__statement_list(stops)
            case "default":
                self.__consume_keyword("default")
                self.__consume_token(TokenKind.COLON)
                consequent = self.__statement_list(stops)
            case _:
                self.tokenizer.print_err(
                    f"expected `case` or `default`, but got {self.lookahead.text}"
                )
        return {"type": "SwitchCase", "test": test, "consequent": consequent}

    def __try_statement(self) -> dict[str, Any]:
        self.__consume_keyword("try")
        block = self.__block_statement()
        handler = self.__catch_clause()

        assert self.lookahead is not None

        finalizer = None

        if self.is_keyword(self.lookahead):
            if self.lookahead.text == "finally":
                self.__consume_keyword("finally")
                finalizer = self.__block_statement()

        return {
            "type": "TryStatement",
            "block": block,
            "handler": handler,
            "finalizer": finalizer,
        }

    def __return_statement(self) -> dict[str, Any]:
        self.__consume_keyword("return")
        arg = self.__expression()

        assert self.lookahead is not None

        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)

        return {"type": "ReturnStatement", "argument": arg}

    def __catch_clause(self) -> dict[str, Any] | None:
        assert self.lookahead is not None

        self.__consume_keyword("catch")

        param = None
        if self.lookahead.kind == TokenKind.OPEN_PAREN:
            self.__consume_token(TokenKind.OPEN_PAREN)
            param = self.__identifier()
            self.__consume_token(TokenKind.CLOSE_PAREN)

        body = self.__block_statement()

        return {"type": "CatchClause", "param": param, "body": body}

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

        return {"type": "DoWhileStatement", "body": body, "condition": condition}

    def __expression_statement(self) -> dict[str, Any]:
        node = {"type": "ExpressionStatement", "expression": self.__expression()}

        assert self.lookahead is not None

        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)

        return node

    def __variable_declaration(self) -> dict[str, Any]:
        assert self.lookahead is not None

        kind = self.__consume_keyword(self.lookahead.text)
        declarations = [self.__variable_declarator(kind.text == "const")]

        while self.lookahead.kind == TokenKind.COMMA:
            self.__consume_token(TokenKind.COMMA)
            declarations.append(self.__variable_declarator(kind.text == "const"))

        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token(TokenKind.SEMICOLON)

        return {
            "type": "VariableDeclaration",
            "kind": kind.text,
            "declarations": declarations,
        }

    def __variable_declarator(self, must_init: bool = False) -> dict[str, Any]:
        assert self.lookahead is not None

        full_line = self.tokenizer.full_line
        id_token = self.lookahead
        id = self.__identifier()

        init = None

        if must_init:
            if self.lookahead.kind != TokenKind.ASSIGNMENT:
                token = Token(
                    "=",
                    TokenKind.ASSIGNMENT,
                    Location(
                        id_token.location.row,
                        id_token.location.col + 1,
                        id_token.location.file_path,
                    ),
                )
                self.tokenizer.print_err("missing initializer", token, full_line)
            self.__consume_token(TokenKind.ASSIGNMENT)
            init = self.__expression()
        elif self.lookahead.kind == TokenKind.ASSIGNMENT:
            self.__consume_token(TokenKind.ASSIGNMENT)
            init = self.__expression()

        return {"type": "VariableDeclarator", "id": id, "init": init}

    def __expression(self) -> dict[str, Any]:
        return self.__assignment_expr()

    def __assignment_expr(self) -> dict[str, Any]:
        left_token = self.lookahead
        node = self.__logic_expr()
        ops = [
            TokenKind.ASSIGNMENT,
            TokenKind.PLUS_ASSIGNMENT,
            TokenKind.MINUS_ASSIGNMENT,
            TokenKind.MUL_ASSIGNMENT,
            TokenKind.DIV_ASSIGNMENT,
            TokenKind.MOD_ASSIGNMENT,
        ]

        assert self.lookahead is not None

        if self.lookahead.kind in ops:
            if node["type"] != "Identifier":
                self.tokenizer.print_err("Invalid left-hand side", left_token)
            node = {
                "type": "AssignmentExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__expression(),
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
                "right": self.__and_expr(),
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
                "right": self.__binary_expr(),
            }
        return node

    def __binary_expr(self) -> dict[str, Any]:
        return self.__comp_expr()

    def __comp_expr(self) -> dict[str, Any]:
        node = self.__add_expr()
        comp_ops = [
            TokenKind.EQUIV,
            TokenKind.NEQUIV,
            TokenKind.EQ,
            TokenKind.NEQ,
            TokenKind.GE,
            TokenKind.LE,
            TokenKind.GT,
            TokenKind.LT,
        ]

        assert self.lookahead is not None

        while self.lookahead.kind in comp_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__add_expr(),
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
                "right": self.__mul_expr(),
            }
        return node

    def __mul_expr(self) -> dict[str, Any]:
        node = self.__pow_expr()
        mul_ops = [TokenKind.MUL, TokenKind.DIV, TokenKind.MOD]

        assert self.lookahead is not None

        while self.lookahead.kind in mul_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__pow_expr(),
            }
        return node

    def __pow_expr(self) -> dict[str, Any]:
        node = self.__unary_expr()

        assert self.lookahead is not None

        while self.lookahead.kind == TokenKind.POW:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token(self.lookahead.kind).text,
                "left": node,
                "right": self.__unary_expr(),
            }
        return node

    def __unary_expr(self) -> dict[str, Any]:
        node: dict[str, Any] = {"type": "UnaryOperator"}

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.PLUS:
                node["operator"] = self.__consume_token(TokenKind.PLUS).text
                node["argument"] = self.__update_expr()
            case TokenKind.MINUS:
                node["operator"] = self.__consume_token(TokenKind.MINUS).text
                node["argument"] = self.__update_expr()
            case _:
                node = self.__update_expr()

        return node

    def __update_expr(self) -> dict[str, Any]:
        assert self.lookahead is not None

        ops = [TokenKind.DECR, TokenKind.INCR]

        if self.lookahead.kind in ops:
            node: dict[str, Any] = {"type": "UpdateExpression", "prefix": True}
            node["operator"] = self.__consume_token(self.lookahead.kind).text
            if self.lookahead.kind != TokenKind.WORD:
                self.tokenizer.print_err(
                    "invalid argument for increment/decrement", self.lookahead
                )
            node["argument"] = self.__identifier()
        else:
            token = self.lookahead
            node = self.__prim_expr()
            if self.lookahead.kind in ops:
                argument = node
                node = {
                    "type": "UpdateExpression",
                    "prefix": False,
                    "operator": self.__consume_token(self.lookahead.kind).text,
                }
                if argument["type"] == "Identifier":
                    node["argument"] = argument
                else:
                    self.tokenizer.print_err(
                        "invalid argument for increment/decrement", token
                    )
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
                    case "true" | "false" | "null":
                        node = self.__literal()
                    case _:
                        node = self.__identifier()
            case _:
                node = self.__literal()
        return node

    def __identifier(self) -> dict[str, Any]:
        ident = self.__consume_token(TokenKind.WORD)
        if not self.is_keyword(ident):
            return {"type": "Identifier", "name": ident.text}
        else:
            self.tokenizer.print_err("unexpected use of keyword", ident)

    def __literal(self) -> dict[str, Any]:

        assert self.lookahead is not None

        match self.lookahead.kind:
            case TokenKind.NUMBER_LIT:
                return self.__numeric_literal()
            case TokenKind.STR_LIT:
                return self.__str_literal()
            case TokenKind.WORD:
                token = self.__consume_token(TokenKind.WORD)
                return {
                    "type": "Literal",
                    "value": None
                    if token.text == "null"
                    else True
                    if token.text == "true"
                    else False,
                    "raw": token.text,
                }
            case _ as text:
                raise AssertionError(f"unreachable: {text}")

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
