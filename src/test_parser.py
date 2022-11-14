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

    def test_power_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("1 ** 2"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "**",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 2,
                            "raw": "2"
                        }
                    }
                }]
            }
        )

    def test_binary_multiplicative_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("1 * 2"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 2,
                            "raw": "2"
                        }
                    }
                }]
            })
        self.assertIsInstance(
            self.parser.parse_string("1 * 2 / 3 % 4"),
            dict  # artinya parsing sukses
        )

    def test_binary_additive_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("1 + 2"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 2,
                            "raw": "2"
                        }
                    }
                }]
            })
        self.assertIsInstance(
            self.parser.parse_string("1 + 2 - 3"),
            dict  # artinya parsing sukses
        )

    def test_binary_comparative_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("1 < 2"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "<",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 2,
                            "raw": "2"
                        }
                    }
                }]
            })
        self.assertIsInstance(
            self.parser.parse_string("1<2<=3>2>=1==1!=0===0!==0"),
            dict  # parsing sukses
        )

    def test_logical_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("true && true"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "LogicalExpression",
                        "operator": "&&",
                        "left": {
                            "type": "Literal",
                            "value": True,
                            "raw": "true"
                        },
                        "right": {
                            "type": "Literal",
                            "value": True,
                            "raw": "true"
                        }
                    }
                }]
            })
        self.assertIsInstance(
            self.parser.parse_string("true && true || false"),
            dict  # parsing sukses
        )

    def test_assignment_expression(self):
        self.assertDictEqual(
            self.parser.parse_string("x = 1"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        }
                    }
                }]
            })
        self.assertIsInstance(
            self.parser.parse_string("x=x+=x-=x*=x/=x%=x"),
            dict  # parsing sukses
        )

    def test_assignment_invalid(self):
        with self.assertRaises(SyntaxError):
            self.parser.parse_string("1 = 2")

    def test_precedence_assignment_or(self):
        # expect or dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("x = true || false"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "right": {
                            "type": "LogicalExpression",
                            "operator": "||",
                            "left": {
                                "type": "Literal",
                                "value": True,
                                "raw": "true"
                            },
                            "right": {
                                "type": "Literal",
                                "value": False,
                                "raw": "false"
                            }
                        }
                    }
                }]
            }
        )

    def test_precedence_or_and(self):
        # expect and dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("true || true && false"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "LogicalExpression",
                        "operator": "||",
                        "left": {
                            "type": "Literal",
                            "value": True,
                            "raw": "true"
                        },
                        "right": {
                            "type": "LogicalExpression",
                            "operator": "&&",
                            "left": {
                                "type": "Literal",
                                "value": True,
                                "raw": "true"
                            },
                            "right": {
                                "type": "Literal",
                                "value": False,
                                "raw": "false"
                            }
                        }
                    }
                }]
            }
        )

    def test_precedence_and_comparative(self):
        # expect comparative dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("true && 1 < 2"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "LogicalExpression",
                        "operator": "&&",
                        "left": {
                            "type": "Literal",
                            "value": True,
                            "raw": "true"
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "<",
                            "left": {
                                "type": "Literal",
                                "value": 1,
                                "raw": "1"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 2,
                                "raw": "2"
                            }
                        }
                    }
                }]
            }
        )

    def test_precedence_comparative_additive(self):
        # expect additive dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("1 < 1 + 1"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "<",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {
                                "type": "Literal",
                                "value": 1,
                                "raw": "1"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 1,
                                "raw": "1"
                            }
                        }
                    }
                }]
            }
        )

    def test_precedence_additive_multiplicative(self):
        # expect multiplicative dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("1+2*3"), {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "*",
                            "left": {
                                "type": "Literal",
                                "value": 2,
                                "raw": "2"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 3,
                                "raw": "3"
                            }
                        }
                    }
                }]
            })

    def test_precedence_multiplicative_power(self):
        # expect ekspresi dalam kurung dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("1 * 2 ** 4"),
            {
                "type":
                "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "**",
                            "left": {
                                "type": "Literal",
                                "value": 2,
                                "raw": "2"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 4,
                                "raw": "4"
                            }
                        }
                    }
                }]
            })

    def test_precedence_power_parenthesized(self):
        self.assertDictEqual(
            self.parser.parse_string("(x = 2) ** 2"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "body": {
                        "type": "BinaryExpression",
                        "operator": "**",
                        "left": {
                            "type": "AssignmentExpression",
                            "operator": "=",
                            "left": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 2,
                                "raw": "2"
                            }
                        },
                        "right": {
                            "type": "Literal",
                            "value": 2,
                            "raw": "2"
                        }
                    }
                }]
            }
        )

    def test_while_statement_block(self):
        self.assertDictEqual(
            self.parser.parse_string("while (x) {}"), {
                "type":
                "Program",
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

    def test_dowhile_statement_block(self):
        self.assertDictEqual(self.parser.parse_string("do {} while (x);"), {
            "type": "Program",
            "body": [{
                "type": "DoWhileStatement",
                "condition": {
                    "name": "x",
                    "type": "Identifier"
                },
                "body": {
                    "body": [],
                    "type": "BlockStatement"
                }
            }]
        })

    def test_dowhile_statement_nonblock(self):
        self.assertDictEqual(self.parser.parse_string("do ; while (x)"), {
            "type": "Program",
            "body": [{
                "type": "DoWhileStatement",
                "condition": {
                    "name": "x",
                    "type": "Identifier"
                },
                "body": {
                    "type": "EmptyStatement"
                }
            }]
        })

    def test_if_statement(self):
        self.assertDictEqual(
            self.parser.parse_string("if (true) ;"), {
                "type": "Program",
                "body": [{
                    "type": "IfStatement",
                    "condition": {
                        "type": "Literal",
                        "value": True,
                        "raw": "true"
                    },
                    "body": {
                        "type": "EmptyStatement"
                    }
                }]
            }
        )

    def test_if_else_statement(self):
        self.assertDictEqual(
            self.parser.parse_string("if (true) ; else ;"), {
                "type": "Program",
                "body": [{
                    "type": "IfStatement",
                    "condition": {
                        "type": "Literal",
                        "value": True,
                        "raw": "true"
                    },
                    "body": {
                        "type": "EmptyStatement"
                    },
                    "alternative": {
                        "type": "EmptyStatement"
                    }
                }]
            }
        )


if __name__ == '__main__':
    unittest.main()
