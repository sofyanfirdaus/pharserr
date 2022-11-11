from pprint import pprint


class WordCFG:

    def __init__(self, rules: dict[str, list[list[str]]]):
        self.rules = rules
        self.symbols = set(rules.keys())

    def evaluate(self, tokens: list[str]) -> bool:
        n = len(tokens)
        table = [[set([]) for _ in range(n)] for _ in range(n)]
        for col in range(n):
            for symbol in self.symbols:
                for transform in self.rules[symbol]:
                    if len(transform) == 1 and transform[0] == tokens[col]:
                        table[0][col].add(symbol)

        for pos in range(1, n):
            for col in range(n - pos):
                for k in range(pos):
                    for symbol in self.symbols:
                        for transform in self.rules[symbol]:
                            if len(transform) == 2 and transform[0] in table[
                                    k][col] and transform[1] in table[
                                        pos - k - 1][col + k + 1]:
                                table[pos][col].add(symbol)
        pprint(table)
        return "S" in table[n - 1][0]


class WordCFGBuilder:

    def __init__(self):
        self.rules: dict[str, list[list[str]]] = {}
        self.__prev_symbol = ""

    def _rule(self, symbol: str, transform_to: str):
        self.rules.setdefault(symbol, [])
        self.rules[symbol].append([transform_to])
        self.__prev_symbol = symbol
        return self

    def _then(self, transform_to: str):
        self.rules[self.__prev_symbol][-1].append(transform_to)
        return self

    def _or(self, transform_to: str):
        self.rules[self.__prev_symbol].append([transform_to])
        return self

    def build(self) -> WordCFG:
        return WordCFG(self.rules)


cfg = WordCFGBuilder()\
        ._rule("S", "NP")._then("VP")\
        ._rule("NP", "Det")._then("N")._or("NP")._then("PP")\
        ._rule("PP", "P")._then("NP")\
        ._rule("VP", "V")._then("NP")._or("VP")._then("PP")\
        ._rule("Det", "the")\
        ._rule("NP", "I")\
        ._rule("N", "man")._or("telescope")._or("cat")._or("dog")._or("pig")\
        ._rule("P", "with")\
        ._rule("V", "saw")\
        .build()

pprint(cfg.rules)
pprint(cfg.evaluate("I saw the cat with the telescope".split()))
