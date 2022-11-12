from tokenizer import TokenKind, Tokenizer, Token
from pprint import pprint as print

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

    def parse_file(self, file_path: str) -> dict:
        self.tokenizer = Tokenizer.from_file(file_path, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program__()

    def __program__(self):
        return {"type": "Program", "body": self.__statement_list__()}

    def __statement_list__(self, until: TokenKind | None = None):
        statements = [self.__statement__()]

        while not self.tokenizer.stop and self.lookahead.kind != until:
            statements.append(self.__statement__())

        return statements

    def __statement__(self):
        match self.lookahead.kind:
            case TokenKind.OPEN_CURLY:
                return self.__block_statement__()
            case _:
                return self.__expression_statement__()

    def __block_statement__(self):
        self.__consume_token__(TokenKind.OPEN_CURLY)
        node = {
            "type": "BlockStatement",
            "body": self.__statement_list__(TokenKind.CLOSE_CURLY)
                    if self.lookahead.kind != TokenKind.CLOSE_CURLY
                    else []
        }
        self.__consume_token__(TokenKind.CLOSE_CURLY)

        return node

    def __expression_statement__(self):
        node = {"type": "ExpressionStatement", "body": self.__expression__()}
        if self.lookahead.kind == TokenKind.SEMICOLON:
            self.__consume_token__(TokenKind.SEMICOLON)
        return node

    def __expression__(self):
        return self.__logic_expr__()

    def __logic_expr__(self):
        return self.__or_expr__()

    def __or_expr__(self):
        node = self.__and_expr__()
        while self.lookahead.kind == TokenKind.OR:
            node = {
                "type": "LogicalExpression",
                "operator": self.__consume_token__(TokenKind.OR).text,
                "left": node,
                "right": self.__and_expr__()
            }
        return node

    def __and_expr__(self):
        node = self.__comp_expr__()
        while self.lookahead.kind == TokenKind.AND:
            node = {
                "type": "LogicalExpression",
                "operator": self.__consume_token__(TokenKind.AND).text,
                "left": node,
                "right": self.__comp_expr__()
            }
        return node

    def __comp_expr__(self):
        node = self.__binary_expr__()
        comp_ops = [
            TokenKind.EQUIV, TokenKind.NEQUIV,
            TokenKind.EQ, TokenKind.NEQ,
            TokenKind.GE, TokenKind.LE,
            TokenKind.GT, TokenKind.LT
        ]
        while self.lookahead.kind in comp_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token__(self.lookahead.kind).text,
                "left": node,
                "right": self.__binary_expr__()
            }
        return node

    def __binary_expr__(self):
        return self.__add_expr__()

    def __add_expr__(self):
        node = self.__mul_expr__()
        add_ops = [TokenKind.PLUS, TokenKind.MINUS]
        while self.lookahead.kind in add_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token__(self.lookahead.kind).text,
                "left": node,
                "right": self.__mul_expr__()
            }
        return node

    def __mul_expr__(self):
        node = self.__prim_expr__()
        mul_ops = [TokenKind.MUL, TokenKind.DIV]
        while self.lookahead.kind in mul_ops:
            node = {
                "type": "BinaryExpression",
                "operator": self.__consume_token__(self.lookahead.kind).text,
                "left": node,
                "right": self.__prim_expr__()
            }
        return node

    def __prim_expr__(self):
        node = {}
        match self.lookahead.kind:
            case TokenKind.OPEN_PAREN:
                self.__consume_token__(TokenKind.OPEN_PAREN)
                node = self.__expression__()
                self.__consume_token__(TokenKind.CLOSE_PAREN)
            case TokenKind.WORD:
                node = self.__identifier__()
            case _:
                node = self.__literal__()
        return node

    def __identifier__(self):
        ident = self.__consume_token__(TokenKind.WORD)
        if not self.isKeyword(ident):
            return {
                "type": "Identifier",
                "name": ident.text
            }
        else:
            self.tokenizer.print_err("unexpected use of keyword", ident)

    def __literal__(self):
        match self.lookahead.kind:
            case TokenKind.NUMBER_LIT: return self.__numeric_literal__()
            case TokenKind.STR_LIT: return self.__str_literal__()

    def __numeric_literal__(self):
        token = self.__consume_token__(TokenKind.NUMBER_LIT)
        return {"type": "NumericLiteral", "value": int(token.text)}

    def __str_literal__(self):
        token = self.__consume_token__(TokenKind.STR_LIT)
        assert len(token.text) >= 2, "unexpected string literal"
        value = token.text[1:-1]
        return {"type": "StringLiteral", "value": value, "raw": token.text}

    def __consume_token__(self, kind: TokenKind) -> Token:
        token = self.tokenizer.expect_token(kind)
        try:
            self.lookahead = self.tokenizer.peek()
        except StopIteration:
            ...
        return token

    def isKeyword(self, token: Token):
        return token.text in KEYWORDS


parser = JSParser()

print(parser.parse_file("test/simple.js"))

# for token in (tokenizer := Tokenizer.from_file("test/inputAcc.js", TOKENS)):
#     if token.kind == TokenKind.WORD and token.text == "if":
#         func_name = tokenizer.expect_token(TokenKind.OPEN_PAREN)
