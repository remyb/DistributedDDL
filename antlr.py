import antlr3
import antlr3.tree 
from sqlLexer import sqlLexer
from sqlParser import sqlParser
import sys

if( len(sys.argv)>1 ):
  char_stream = antlr3.ANTLRFileStream(sys.argv[1])
else:
  char_stream = antlr3.ANTLRStringStream(raw_input("SQL>"))
lexer = sqlLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = sqlParser(tokens)
r = parser.createtablestmt()

print "tablename = " + r.tree.children[2].toString()
print "tree = " + r.tree.toStringTree()


