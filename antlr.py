#!/usr/bin/python

import antlr3
import antlr3.tree 
from sqlLexer import sqlLexer
from sqlParser import sqlParser
import sys

# Uses ANTLR to Parse SQL Grammer.
class GrammerParse:
  def __init__(self, sql):
    self.sql =  sql
    self.tree = ""
    self.table = ""
    self.command = ""
  def parse(self):
    stream = antlr3.ANTLRFileStream(self.sql)
    lexer = sqlLexer(stream)
    tokens = antlr3.CommonTokenStream(lexer)
    parser = sqlParser(tokens)
    r = parser.sqlstmt()
    self.tree = r.tree.toStringTree()
    if( r.tree.children[0].toString().lower() == "create"):
      self.table = r.tree.children[2].toString()
      self.command = "CREATE"
    elif( r.tree.children[0].toString().lower() == "select"):
      self.table = r.tree.children[3].toString()
      self.command = "SELECT"
    elif( r.tree.children[0].toString().lower() == "drop"):
      self.table = r.tree.children[1].toString()
      self.command = "DROP" 

if __name__ == '__main__':
  if( len(sys.argv)>1 ):
    sql = sys.argv[1]
  else:
    sql = raw_input("SQL>")
  result = GrammerParse(sql)
  result.parse()
  print "Tree is: " + result.tree
  print "Table is " + result.table
  print "Command is " + result.command
  
