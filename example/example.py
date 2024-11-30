# this will not work when lex.py is not in this folder. if you are planning to
# use this example, make sure to move lex.py in to this folder first

from lex import tokenise

print(tokenise("rules.lexif", "test_code.txt"))