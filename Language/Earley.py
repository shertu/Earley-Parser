from Language.Grammar import *

class EarleyItem:
    dotSymbol = '•'

    def __init__(self, r, dot = 0, fromChart = 0):
        assert isinstance(r, Rule)
        assert isinstance(dot, int)
        assert isinstance(fromChart, int)

        assert (0 <= dot <= len(r.t))
        assert (0 <= fromChart)

        self.r = r
        self.dot = dot
        self.fromChart = fromChart

    def __repr__(self):
        tList = self.r.t.copy()
        assert isinstance(tList, list)

        tList.insert(self.dot, self.dotSymbol)
        aString = "{0} -> {1}".format(self.r.f, tList)
        bString = "{0} from {1}".format(aString, self.fromChart)

        return bString

    @property
    def nextChar(self):
        if (self.dot < len(self.r.t)):
            return self.r.t[self.dot]

    @property
    def fromChar(self):
        return (self.r.f[0])

    @property
    def isComplete(self):
        return (len(self.r.t) == self.dot)

    def __eq__(self, other):
        if (isinstance(other, EarleyItem)):
            if (self.__dict__ == other.__dict__):
                return True

        return False

    def shift(self):
        return EarleyItem(self.r, self.dot + 1, self.fromChart)

class Parser:
    def __init__(self, grammar):
        assert isinstance(grammar, Grammar_2)
        self.grammar = grammar

        self.grammar_C = self.grammar.characters
        self.grammar_T = self.grammar.terminals
        self.grammar_N = self.grammar.nonTerminals

        self.grammarAug_newStart = self.newChar('S')
        self.grammarAug_endString = self.newChar('$')

    def newChar(self, baseChar):
        assert isinstance(baseChar, str)

        while (baseChar in self.grammar_C):
            baseChar += '\''
        return baseChar

    def parse(self, s):
        for c in s:
            assert isinstance(c, str)

        print("\nParsing " + s + " ...\n")

        # Terminal check
        for c in s:
            if (c not in self.grammar_T):
                return False

        # The set up
        s += self.grammarAug_endString
        self.charts = [[] for i in range(len(s))]
        self.charts[0].append(EarleyItem(Rule([self.grammar.s], [self.grammarAug_newStart])))

        # The parse
        for k in range(len(s)):
            e = 0
            while (e < len(self.charts[k])):
                earleyItem = self.charts[k][e]
                assert isinstance(earleyItem, EarleyItem)
                if not (earleyItem.isComplete):
                    if (earleyItem.nextChar in self.grammar_N):
                        print(k, "p", earleyItem)
                        self.predictor(earleyItem, k)    # non-terminal
                    else:
                        print(k, "s", earleyItem)
                        self.scanner(earleyItem, k, s)    # terminal
                else:
                    print(k, "c", earleyItem)
                    self.completer(earleyItem, k)    # complete parse

                e += 1

        print()
        for k in range(len(self.charts)):
            print(k, self.charts[k])

        # Output
        res = False
        for r in self.charts[-1]:
            assert isinstance(r, EarleyItem)
            if (r.fromChart == 0):
                if (r.fromChar == self.grammarAug_newStart):
                    if (r.isComplete):
                        res = True

        return res

    def predictor(self, earleyItem, k):
        assert isinstance(earleyItem, EarleyItem)
        assert isinstance(k, int)

        nextChar = earleyItem.nextChar

        assert (0 <= k)
        assert (nextChar in self.grammar_N)

        for r in self.grammar.getFromRule(nextChar):
            self.addToChart(EarleyItem(r, 0, k), k)

    def scanner(self, earleyItem, k, s):
        assert isinstance(earleyItem, EarleyItem)
        assert isinstance(k, int)

        for c in s:
            assert isinstance(c, str)

        nextChar = earleyItem.nextChar

        assert (0 <= k)
        assert (nextChar in self.grammar_T)

        if (earleyItem.nextChar == s[k]):
            self.addToChart(earleyItem.shift(), k + 1)

    def completer(self, earleyItem, k):
        assert isinstance(earleyItem, EarleyItem)
        assert isinstance(k, int)

        nextChar = earleyItem.nextChar

        assert (0 <= k)
        assert (nextChar is None)

        for r in self.charts[earleyItem.fromChart]:
            assert isinstance(r, EarleyItem)

            if (r.nextChar == earleyItem.fromChar):
                self.addToChart(r.shift(), k)

    def addToChart(self, earleyItem, k):
        assert isinstance(earleyItem, EarleyItem)
        assert isinstance(k, int)

        if (earleyItem not in self.charts[k]):
            self.charts[k].append(earleyItem)
