#!/usr/bin/python

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

r = parser.sqlstmt()

if( r.tree.children[0].toString().lower() == "create"):
  print "tablename = " + r.tree.children[2].toString()
  print "tree = " + r.tree.toStringTree()
elif( r.tree.children[0].toString().lower() == "select"):
  print "tablename = " + r.tree.children[3].toString()
  print "tree = " + r.tree.toStringTree()
elif( r.tree.children[0].toString().lower() == "drop"):
  print "tablename = " + r.tree.children[1].toString()
  print "tree = " + r.tree.toStringTree() 


