import unittest
from js_parser import JSParser


class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = JSParser()

    def test_empty(self):
        self.assertDictEqual(self.parser.parse_string(""), {
            "type": "Program",
            "body": []
        })

    def test_numeric_literal(self):
        self.assertDictEqual(
            self.parser.parse_string("1"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "NumericLiteral",
                        "value": 1
                    }
                }]
            })

    def test_string_literal(self):
        self.assertDictEqual(
            self.parser.parse_string('"ini string"'), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "StringLiteral",
                        "value": "ini string",
                        "raw": '"ini string"'
                    }
                }]
            })
        self.assertDictEqual(
            self.parser.parse_string("'ini string'"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "StringLiteral",
                        "value": "ini string",
                        "raw": "'ini string'"
                    }
                }]
            })
        self.assertDictEqual(
            self.parser.parse_string("`ini string`"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "StringLiteral",
                        "value": "ini string",
                        "raw": "`ini string`"
                    }
                }]
            })

    # test statement
    def test_empty_statement(self):
        self.assertDictEqual(self.parser.parse_string(";"), {
            "type": "Program",
            "body": [{
                "type": "EmptyStatement"
            }]
        })

    def test_while_statement_block(self):
        self.assertDictEqual(self.parser.parse_string("while (x) {}"), {
            "type": "Program",
            "body": [{
                "type": "WhileStatement",
                "condition": {
                    "name": "x",
                    "type": "Identifier"
                },
                "body": {
                    "body": [],
                    "type": "BlockStatement"
                },
                }]
            })

    def test_while_statement_nonblock(self):
        self.assertDictEqual(self.parser.parse_string("while (x) ;"), {
            "type": "Program",
            "body": [{
                "type": "WhileStatement",
                "condition": {
                    "name": "x",
                    "type": "Identifier"
                },
                "body": {
                    "type": "EmptyStatement"
                }
            }]
        })


if __name__ == '__main__':
    unittest.main()
