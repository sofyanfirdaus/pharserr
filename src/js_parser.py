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
    TokenKind.EQUIV: "===",
    TokenKind.EQ: "==",
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
    TokenKind.OR: "||"
}


class JSParser:

    def parse_file(self, file_path: str) -> dict:
        self.tokenizer = Tokenizer.from_file(file_path, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program__()

    def __program__(self):
        node = {"type": "Program"}
        statements = [self.__statement__()]

        while not self.tokenizer.stop:
            statements.append(self.__statement__())

        node["body"] = statements

        return node

    def __statement__(self):
        return self.__expression__()

    def __expression__(self):
        return self.__logic_expr__()

    def __logic_expr__(self):
        return self.__or_expr__()

    def __or_expr__(self):
        node = self.__and_expr__()
        while self.lookahead.kind == TokenKind.OR:
            node = {
                "type": "LogicalExpression",
                "left": node,
                "operator": "||"
            }
            self.__consume_token__(TokenKind.OR)
            node["right"] = self.__and_expr__()
        return node

    def __and_expr__(self):
        node = self.__binary_expr__()
        while self.lookahead.kind == TokenKind.AND:
            node = {
                "type": "LogicalExpression",
                "left": node,
                "operator": "&&"
            }
            self.__consume_token__(TokenKind.AND)
            node["right"] = self.__binary_expr__()
        return node

    def __binary_expr__(self):
        return self.__add_expr__()

    def __add_expr__(self):
        node = self.__mul_expr__()
        while self.lookahead.kind == TokenKind.PLUS or self.lookahead.kind == TokenKind.MINUS:
            node = {
                "type": "BinaryExpression",
                "left": node
            }
            match self.lookahead.kind:
                case TokenKind.PLUS:
                    self.__consume_token__(TokenKind.PLUS)
                    node["operator"] = "+"
                case TokenKind.MINUS:
                    node["operator"] = "-"
                    self.__consume_token__(TokenKind.MINUS)
            node["right"] = self.__mul_expr__()
        return node

    def __mul_expr__(self):
        node = self.__prim_expr__()
        while self.lookahead.kind == TokenKind.MUL or self.lookahead.kind == TokenKind.DIV:
            node = {
                "type": "BinaryExpression",
                "left": node
            }
            match self.lookahead.kind:
                case TokenKind.MUL:
                    node["operator"] = "*"
                    self.__consume_token__(TokenKind.MUL)
                case TokenKind.DIV:
                    node["operator"] = "/"
                    self.__consume_token__(TokenKind.DIV)
            node["right"] = self.__prim_expr__()
        return node

    def __prim_expr__(self):
        node = {}
        if self.lookahead.kind == TokenKind.OPEN_PAREN:
            self.__consume_token__(TokenKind.OPEN_PAREN)
            node = self.__expression__()
            self.__consume_token__(TokenKind.CLOSE_PAREN)
        else:
            node = self.__literal__()
        return node

    def __literal__(self):
        if self.lookahead is not None:
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


parser = JSParser()

print(parser.parse_file("test/simple.js"))

# for token in (tokenizer := Tokenizer.from_file("test/inputAcc.js", TOKENS)):
#     if token.kind == TokenKind.WORD and token.text == "if":
#         func_name = tokenizer.expect_token(TokenKind.OPEN_PAREN)
