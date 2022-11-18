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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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

    def test_update_expression_noprefix(self):
        self.assertDictEqual(
            self.parser.parse_string("x++"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "UpdateExpression",
                        "prefix": False,
                        "operator": "++",
                        "argument": {
                            "type": "Identifier",
                            "name": "x"
                        }
                    }
                }]
            }
        )
        self.assertIsInstance(
            self.parser.parse_string("x++;x--"),
            dict
        )

    def test_update_expression_prefix(self):
        self.assertDictEqual(
            self.parser.parse_string("++x"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "UpdateExpression",
                        "prefix": True,
                        "operator": "++",
                        "argument": {
                            "type": "Identifier",
                            "name": "x"
                        }
                    }
                }]
            }
        )
        self.assertIsInstance(
            self.parser.parse_string("++x;--x"),
            dict
        )

    def test_update_expression_invalid(self):
        with self.assertRaises(SyntaxError):
            self.parser.parse_string("1++")
        with self.assertRaises(SyntaxError):
            self.parser.parse_string("++1")

    def test_precedence_assignment_or(self):
        # expect or dievaluasi duluan
        self.assertDictEqual(
            self.parser.parse_string("x = true || false"), {
                "type": "Program",
                "body": [{
                    "type": "ExpressionStatement",
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "expression": {
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
                    "consequent": {
                        "type": "EmptyStatement"
                    },
                    "alternate": None
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
                    "consequent": {
                        "type": "EmptyStatement"
                    },
                    "alternate": {
                        "type": "EmptyStatement"
                    }
                }]
            }
        )

    def test_try_statement_param(self):
        self.assertDictEqual(
            self.parser.parse_string("try {} catch (x) {}"), {
                "type": "Program",
                "body": [{
                    "type": "TryStatement",
                    "block": {
                        "type": "BlockStatement",
                        "body": []
                    },
                    "handler": {
                        "type": "CatchClause",
                        "param": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "body": {
                            "type": "BlockStatement",
                            "body": []
                        }
                    },
                    "finalizer": None
                }]
            }
        )

    def test_try_statement_noparam(self):
        self.assertDictEqual(
            self.parser.parse_string("try {} catch {}"), {
                "type": "Program",
                "body": [{
                    "type": "TryStatement",
                    "block": {
                        "type": "BlockStatement",
                        "body": []
                    },
                    "handler": {
                        "type": "CatchClause",
                        "param": None,
                        "body": {
                            "type": "BlockStatement",
                            "body": []
                        }
                    },
                    "finalizer": None
                }]
            }
        )

    def test_try_statement_finalizer(self):
        self.assertDictEqual(
            self.parser.parse_string("try {} catch {} finally {}"), {
                "type": "Program",
                "body": [{
                    "type": "TryStatement",
                    "block": {
                        "type": "BlockStatement",
                        "body": []
                    },
                    "handler": {
                        "type": "CatchClause",
                        "param": None,
                        "body": {
                            "type": "BlockStatement",
                            "body": []
                        }
                    },
                    "finalizer": {
                        "type": "BlockStatement",
                        "body": []
                    }
                }]
            }
        )

    def test_variable_declaration(self):
        self.assertDictEqual(
            self.parser.parse_string("let x = 1;"), {
                "type": "Program",
                "body": [{
                    "type": "VariableDeclaration",
                    "kind": "let",
                    "declarations": [{
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "init": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        }
                    }]
                }]
            }
        )
        self.assertDictEqual(
            self.parser.parse_string("var x = 1"), {
                "type": "Program",
                "body": [{
                    "type": "VariableDeclaration",
                    "kind": "var",
                    "declarations": [{
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "init": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        }
                    }]
                }]
            }
        )
        self.assertDictEqual(
            self.parser.parse_string("const x = 1"), {
                "type": "Program",
                "body": [{
                    "type": "VariableDeclaration",
                    "kind": "const",
                    "declarations": [{
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "init": {
                            "type": "Literal",
                            "value": 1,
                            "raw": "1"
                        }
                    }]
                }]
            }
        )

    def test_variable_declaration_noinit(self):
        self.assertDictEqual(
            self.parser.parse_string("let x"), {
                "type": "Program",
                "body": [{
                    "type": "VariableDeclaration",
                    "kind": "let",
                    "declarations": [{
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "init": None
                    }]
                }]
            }
        )

    def test_variable_declaration_list(self):
        self.assertDictEqual(
            self.parser.parse_string("let x = 1, y"), {
                "type": "Program",
                "body": [{
                    "type": "VariableDeclaration",
                    "kind": "let",
                    "declarations": [
                        {
                            "type": "VariableDeclarator",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": {
                                "type": "Literal",
                                "value": 1,
                                "raw": "1"
                            }
                        },
                        {
                            "type": "VariableDeclarator",
                            "id": {
                                "type": "Identifier",
                                "name": "y"
                            },
                            "init": None
                        }
                    ]
                }]
            }
        )

    def test_for_statement(self):
        self.assertDictEqual(
            self.parser.parse_string(("for (x;x;x) ;")), {
                "type": "Program",
                "body": [{
                    "type": "ForStatement",
                    "init": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "test": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "update": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "body": {
                        "type": "EmptyStatement"
                    }
                }]
            }
        )

    def test_for_statement_variable_declaration(self):
        self.assertDictEqual(
            self.parser.parse_string("for (let x;x;x) ;"), {
                "type": "Program",
                "body": [{
                    "type": "ForStatement",
                    "init": {
                        "type": "VariableDeclaration",
                        "kind": "let",
                        "declarations": [{
                            "type": "VariableDeclarator",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": None
                        }]
                    },
                    "test": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "update": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "body": {
                        "type": "EmptyStatement"
                    }
                }]
            }
        )

    def test_for_statement_empty(self):
        self.assertDictEqual(
            self.parser.parse_string("for (;;) {}"), {
                "type": "Program",
                "body": [{
                    "type": "ForStatement",
                    "init": None,
                    "test": None,
                    "update": None,
                    "body": {
                        "type": "BlockStatement",
                        "body": []
                    }
                }]
            }
        )

    def test_return_statement(self):
        self.assertDictEqual(
            self.parser.parse_string("return x;"), {
                "type": "Program",
                "body": [{
                    "type": "ReturnStatement",
                    "argument": {
                        "type": "Identifier",
                        "name": "x"
                    }
                }]
            }
        )

    def test_switch_statement_empty(self):
        self.assertDictEqual(
            self.parser.parse_string("switch (x) {}"), {
                "type": "Program",
                "body": [{
                    "type": "SwitchStatement",
                    "discriminant": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "cases": []
                }]
            }
        )

    def test_switch_statement_case(self):
        self.assertDictEqual(
            self.parser.parse_string("switch (x) {case y: z}"), {
                "type": "Program",
                "body": [{
                    "type": "SwitchStatement",
                    "discriminant": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "cases": [{
                        "type": "SwitchCase",
                        "test": {
                            "type": "Identifier",
                            "name": "y"
                        },
                        "consequent": [{
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "Identifier",
                                "name": "z"
                            }
                        }]
                    }]
                }]
            }
        )

    def test_switch_statement_default(self):
        self.assertDictEqual(
            self.parser.parse_string("switch (x) {default: z}"), {
                "type": "Program",
                "body": [{
                    "type": "SwitchStatement",
                    "discriminant": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "cases": [{
                        "type": "SwitchCase",
                        "test": None,
                        "consequent": [{
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "Identifier",
                                "name": "z"
                            }
                        }]
                    }]
                }]
            }
        )

    def test_switch_statement_case_list(self):
        self.assertDictEqual(
            self.parser.parse_string("switch (x) {case y: z; default: w}"), {
                "type": "Program",
                "body": [{
                    "type": "SwitchStatement",
                    "discriminant": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "cases": [
                        {
                            "type": "SwitchCase",
                            "test": {
                                "type": "Identifier",
                                "name": "y"
                            },
                            "consequent": [{
                                "type": "ExpressionStatement",
                                "expression": {
                                    "type": "Identifier",
                                    "name": "z"
                                }
                            }]
                        },
                        {
                            "type": "SwitchCase",
                            "test": None,
                            "consequent": [{
                                "type": "ExpressionStatement",
                                "expression": {
                                    "type": "Identifier",
                                    "name": "w"
                                }
                            }]
                        }
                    ]
                }]
            }
        )


if __name__ == '__main__':
    unittest.main()
