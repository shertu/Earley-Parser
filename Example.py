from Language.Earley import Parser
from Language.Grammar import Grammar_2

"""
Process
"""

while (__name__ == "__main__"):
    aGrammar = Grammar_2()

    aGrammar.setStart('S')
    aGrammar.addRule([], ['S'])
    aGrammar.addRule(['A'], ['S'])
    aGrammar.addRule(['A', 'A'], ['A'])
    aGrammar.addRule(['a'], ['A'])

    print(aGrammar)
    aParser = Parser(aGrammar)
    print("\n" + str(aParser.parse("aaa")))

    exit()
