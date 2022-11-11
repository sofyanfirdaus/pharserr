from tokenizer import TokenKind, Tokenizer

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
    TokenKind.AND: "&&"
}


class JSParser:

    def parse_file(self, file_path: str) -> dict:
        self.tokenizer = Tokenizer.from_file(file_path, TOKENS)
        self.lookahead = self.tokenizer.peek()
        return self.__program__()

    def __program__(self):
        node = {"type": "Program", "body": self.__literal__()}
        return node

    def __literal__(self):
        if self.lookahead is not None:
            match self.lookahead.kind:
                case TokenKind.NUMBER_LIT: return self.__numeric_literal__()
                case TokenKind.STR_LIT: return self.__str_literal__()

    def __numeric_literal__(self):
        token = self.tokenizer.expect_token(TokenKind.NUMBER_LIT, "number")
        return {"type": "NumericLiteral", "value": int(token.text)}

    def __str_literal__(self):
        token = self.tokenizer.expect_token(TokenKind.STR_LIT, "string")
        assert len(token.text) >= 2, "unexpected string literal"
        value = token.text[1:-1]
        return {"type": "StringLiteral", "value": value, "raw": token.text}


parser = JSParser()

# print(parser.parse_file("test/simple.js"))

for token in (tokenizer := Tokenizer.from_file("test/inputAcc.js", TOKENS)):
    if token.kind == TokenKind.WORD and token.text == "if":
        func_name = tokenizer.expect_token(TokenKind.OPEN_PAREN)
