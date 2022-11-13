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
                        "type": "Literal",
                        "value": 1,
                        "raw": "1"
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
                        "type": "Literal",
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
                        "type": "Literal",
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
                        "type": "Literal",
                        "value": "ini string",
                        "raw": "`ini string`"
                    }
                }]
            })

    def test_boolean_literal(self):
        self.assertDictEqual(
            self.parser.parse_string("true"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "Literal",
                        "value": True,
                        "raw": "true"
                    }
                }]
            })
        self.assertDictEqual(
            self.parser.parse_string("false"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "Literal",
                        "value": False,
                        "raw": "false"
                    }
                }]
            })

    # test statement list
    def test_statement_list(self):
        self.assertDictEqual(
            self.parser.parse_string(";\n;"), {
                "type": "Program",
                "body": [{
                    "type": "EmptyStatement"
                }, {
                    "type": "EmptyStatement"
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

    def test_empty_block_statement(self):
        self.assertDictEqual(self.parser.parse_string("{}"), {
            "type": "Program",
            "body": [{
                "type": "BlockStatement",
                "body": []
            }]
        })

    def test_block_statement(self):
        self.assertDictEqual(
            self.parser.parse_string("{;}"), {
                "type":
                "Program",
                "body": [{
                    "type": "BlockStatement",
                    "body": [{
                        "type": "EmptyStatement",
                    }]
                }]
            })


if __name__ == '__main__':
    unittest.main()
