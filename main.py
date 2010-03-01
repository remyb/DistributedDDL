#!/usr/bin/python

#Remy Baumgarten
#Kevin Chiogioji

import ibm_db
import antlr3
import antlr3.tree 
from sqlLexer import sqlLexer
from sqlParser import sqlParser
import ConfigParser

#show stats on database
def client_print(db): 
  client = ibm_db.client_info(db)
  print "DRIVER_NAME: string(%d) \"%s\"" % (len(client.DRIVER_NAME), client.DRIVER_NAME)
  print "DRIVER_VER: string(%d) \"%s\"" % (len(client.DRIVER_VER), client.DRIVER_VER)
  print "DATA_SOURCE_NAME: string(%d) \"%s\"" % (len(client.DATA_SOURCE_NAME), client.DATA_SOURCE_NAME)
  print "DRIVER_ODBC_VER: string(%d) \"%s\"" % (len(client.DRIVER_ODBC_VER), client.DRIVER_ODBC_VER)
  print "ODBC_VER: string(%d) \"%s\"" % (len(client.ODBC_VER), client.ODBC_VER)
  print "ODBC_SQL_CONFORMANCE: string(%d) \"%s\"" % (len(client.ODBC_SQL_CONFORMANCE), client.ODBC_SQL_CONFORMANCE)
  print "APPL_CODEPAGE: int(%s)" % client.APPL_CODEPAGE
  print "CONN_CODEPAGE: int(%s)" % client.CONN_CODEPAGE

def config_extract(settings,section):
  config = ConfigParser.RawConfigParser()
  config.read(settings)
  try:
    options = config.options(section)
  except:
    print "[*] The file is not in the correct format, please consult readme"
    sys.exit()
  items= {}
  for option in options:
    try:
      items[option] = config.get(section, option)
      if items[option] == -1:
        DebugPrint("skip: %s" % option)
    except:
      print("exception on %s!" % option)
      items[option] = None
  return items  
  
# execute query
def exec_query(db, query):
  try:
    ibm_db.exec_immediate(db,query)
  except:
    print "[*] The transaction could not be completed:", query# ,ibm_db.stmt_errormsg()
  else:
    print "[*] Transaction complete: ",query
    
    

# check to see if dtables in CATALOG exists, if not, create it
def create_catalog(cat, catalog):
  try:
    ibm_db.exec_immediate(cat,"create table dtables (tname char(32), nodedriver char(64), " \
                              "nodeurl char(128), nodeuser char(16), nodepasswd char(16), " \
                              "partmtd int, nodeid int, partcol char(32), partparam1 char(32)," \
                              " partparam2 char(32))")
  except:
    print "[*] NOTICE catalog table exists, continuing..."

# insert metadata
def insert_catalog_row(query, conn, node_conf, nodeid):
  #index = query.split()
  #if index[0].upper() == "create" or index[0].upper() == "DROP":
  #  tableName = index[2]  
  #elif index[0] == "select":
  #  tableName = index[3]
  #print tableName,"=============="
  #if tableName.find("(") != -1:
  #  tableName = tableName[0:tableName.find("(")]
  tableName = get_table(query) 
  #print tableName    
  cat_row = "INSERT INTO dtables (tname, nodedriver, nodeurl, nodeuser," \
    " nodepasswd, partmtd, nodeid, partcol, partparam1, partparam2) VALUES" \
    " ('%s', '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s');" % (tableName, node_conf["driver"], node_conf["hostname"], node_conf["username"], node_conf["passwd"], "NULL", nodeid, "NULL", "NULL", "NULL")  
  #print cat_row
  stmt = ibm_db.exec_immediate(conn,cat_row)
  print "[*] Cataloging transaction...done"

# read DDLs from file
def readDDL(fileName):
  try:
    f = open(fileName,'r')
    commands = f.readlines()
    for command in commands:
      #if len(command) < 2:
        #commands.pop()
      command = command.rstrip()
    print commands, "returning commands"
    return commands
  except:
    print "the file could not be read\n"
  else:
    f.close()

# Prints the contents of the Query
def print_results(conn,sql):
	#sql = "SELECT " + column + " FROM " + table + ";"
	#print sql
	stmt = ibm_db.exec_immediate(conn,sql)
	dictionary = ibm_db.fetch_assoc(stmt)
	while dictionary != False:
		print '==================='
		print "ISBN: ", dictionary["ISBN"]
		print "Title: ",dictionary["TITLE"]
		print "Author: ",dictionary["AUTHOR"]
		dictionary = ibm_db.fetch_assoc(stmt)

# Get nodes from catalog for a specific table
# and return it as a list (url, user,passwd)
def get_nodes(conn,tablename):
  sql = "SELECT DISTINCT * FROM DTABLES WHERE TNAME = '" + tablename + "';"
  print "\t",sql
  stmt = ibm_db.exec_immediate(conn,sql)
  dictionary = ibm_db.fetch_assoc(stmt)
  nodes = []
  while dictionary != False:
    url = dictionary["NODEURL"].rstrip()
    user = dictionary["NODEUSER"]
    passwd = dictionary["NODEPASSWD"]
    driver = dictionary["NODEDRIVER"]
    node = (url,user,passwd,driver)
    nodes.append(node)
    dictionary = ibm_db.fetch_assoc(stmt)
  return nodes
		
# returns a list of tuples for each line in the csv file
def loadCSV(filename):
  contents = []
  for line in open(filename):
    fields = line.split(',');
    number = fields[0]
    title = fields[1]
    author = fields[2]
    book = (number,title,author)
    contents.append(book)
  return contents

# parse to obtain tablename
def get_table(sql):
  stream = antlr3.ANTLRStringStream(sql)
  lexer = sqlLexer(stream)
  tokens = antlr3.CommonTokenStream(lexer)
  parser = sqlParser(tokens)
  r = parser.sqlstmt()
  tree = r.tree.toStringTree()
  if( r.tree.children[0].toString().lower() == "create"):
    return r.tree.children[2].toString()
  elif( r.tree.children[0].toString().lower() == "select"):
    return r.tree.children[3].toString()
  elif( r.tree.children[0].toString().lower() == "drop"):
    return r.tree.children[1].toString()
