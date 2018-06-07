"""
Contributors:
    Jared Blackman
Update:
    2017-06-07
"""

"""
An r for the Graph class
"""

class Rule:
    def __init__(self, t, f):
        # Type checking the TO and FROM vertices
        for c in t:
            assert isinstance(c, str)
        for c in f:
            assert isinstance(c, str)

        self.t = t
        self.f = f

    def __repr__(self):
        aString = "{0} -> {1}".format(self.f, self.t)

        return aString

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        if (isinstance(other, Rule)):
            if (self.__dict__ == other.__dict__):
                return True

        return False

""""""
class Grammar_0:
    def __init__(self):
        self.r = set()
        self.s = None

    def setStart(self, v):
        assert isinstance(v, str)
        self.s = v

    def addRule(self, t, f):
        r = Rule(t, f)
        self.r.add(r)

    def delRule(self, r):
        try:
            self.r.remove(r)
        except:
            raise ValueError("The rule " + str(r) + " does not exist")

    def __repr__(self):
        aDict = {'r': self.r, 's': self.s}
        return str(aDict)

    """
    Extra Methods
    """

    @property
    def characters(self):
        cSet = set()

        for r in self.r:
            for c in r.t:
                cSet.add(c)

            for c in r.f:
                cSet.add(c)

        return cSet

    def __copy__(self):
        aGrammarClass = self.__class__
        aGrammar = self.__class__()

        aGrammarClass.setStart(aGrammar, self.s)

        for r in self.r:
            aGrammarClass.addRule(aGrammar, r.t, r.f)

        return aGrammar


""""""
class Grammar_1(Grammar_0):
    def __init__(self):
        Grammar_0.__init__(self)

        self.emptyEdge = False
        self.antiEmptyEdge = False
        self.nonTerminals = set()

    def setStart(self, v):
        Grammar_0.setStart(self, v)
        self._updateAttributes()

    def addRule(self, t, f):
        Grammar_0.addRule(self, t, f)
        self._checkRule(t, f)

    def delRule(self, r):
        Grammar_0.delRule(self, r)
        self._updateAttributes()

    def _checkRule(self, t, f):

        check_one = False

        fLen = len(f)
        tLen = len(t)

        if (tLen >= fLen):
            for i in range(fLen):
                a1 = f[:i]
                b1 = f[i + 1:]

                temp = tLen - len(b1)

                a2 = t[:i]
                b2 = t[temp:]


                if (a1 == a2 and b1 == b2):
                    check_one = True
                    nT = f[i]
                    break

        if not (check_one):
            assert (self.s is not None)

            if (t == [] and f == [self.s]):
                self.emptyEdge = True
                nT = self.s
            else:
                raise ValueError("Grammar is not context sensitive")

        self.nonTerminals.add(nT)

        # Empty string
        for c in t:
            if (c == self.s):
                self.antiEmptyEdge = True

        if (self.emptyEdge and self.antiEmptyEdge):
            raise ValueError("Grammar is not context sensitive")

    def _updateAttributes(self):
        self.emptyEdge = False
        self.antiEmptyEdge = False
        self.nonTerminals = set()

        for r in self.r:
            self._checkRule(r.t, r.f)

    """
    Extra Methods
    """

    @property
    def terminals(self):
        return (self.characters - self.nonTerminals)

""""""
class Grammar_2(Grammar_1):
    def _checkRule(self, t, f):
        Grammar_1._checkRule(self, t, f)

        if (len(f) > 1):
            raise ValueError("Grammar is not context free")

    """
    Extra Methods
    """

    def getFromRule(self, f):
        assert isinstance(f, str)
        assert (f in self.nonTerminals)

        fSet = set()

        for r in self.r:
            if (r.f[0] == f):
                fSet.add(r)

        return fSet

""""""
class Grammar_3(Grammar_2):
    def __init__(self):
        Grammar_2.__init__(self)

        self.RRG = False
        self.LRG = False

    def _checkRule(self, t, f):
        Grammar_2._checkRule(self, t, f)

        tLen = len(t)

        for i in range(tLen):
            c = t[i]

            cPrev = None
            cNext = None

            if (i > 0):
                cPrev = t[i - 1]

            if (i < tLen - 1):
                cNext = t[i + 1]

            if (c in self.nonTerminals):
                if (cPrev is not None and cPrev not in self.nonTerminals):
                    self.LRG = True

                if (cNext is not None and cNext not in self.nonTerminals):
                    self.RRG = True

        if (self.RRG and self.LRG):
            raise ValueError("Grammar is not regular")

    def _updateAttributes(self):
        self.RRG = False
        self.LRG = False

        Grammar_2._updateAttributes(self)
