#!/usr/bin/python

#Remy Baumgarten
#Kevin Chiogioji

import ibm_db

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


# execute query
def exec_query(db, query):
  try:
    ibm_db.exec_immediate(db,query)
  except:
    print "[*] The transaction could not be completed:", query #ibm_db.stmt_errormsg()
  else:
    print "[*] Transaction complete: ",query

# check to see if dtables in CATALOG exists, if not, create it
def create_catalog(cat, catalog):
  try:
    ibm_db.exec_immediate(cat,"CREATE TABLE "+catalog['table'])
  except:
    print "[*] NOTICE catalog table exists, continuing..."

# insert metadata
def insert_catalog_row(query, conn, node_conf):
  index = query.split()
  if index[0].upper() == "CREATE" or index[0].upper() == "DROP":
    tableName = index[2]  
  elif index[0].upper() == "SELECT":
    tableName = index[3]
      
  if tableName.find("(") != -1:
    tableName = tableName[0:tableName.find("(")]
       
  cat_row = "INSERT INTO dtables (tname, nodedriver, nodeurl, nodeuser," \
    " nodepasswd, partmtd, partparam1, partparam2) VALUES ('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s');" % (tableName.rstrip(";"), node_conf["driver"], node_conf ["hostname"], node_conf["username"], node_conf["passwd"], "NULL", "NULL", "NULL")  
  #print cat_row
  stmt = ibm_db.exec_immediate(conn,cat_row)
  print "[*] Cataloging transaction...done"

# read DDLs from file
def readDDL(fileName):
  try:
    f = open(fileName,'r')
    commands = f.readlines()
    for command in commands:
      command = command.strip()
    return commands
  except:
    print "the file could not be read\n"
  else:
    f.close()

def print_table(conn, column, table):
	sql = "SELECT " + column + " FROM " + table + ";"
	print sql
	stmt = ibm_db.exec_immediate(conn,sql)
	dictionary = ibm_db.fetch_assoc(stmt)
	while dictionary != False:
		print '==================='
		print "ISBN: ", dictionary["ISBN"]
		print "Title: ",dictionary["TITLE"]
		print "Author: ",dictionary["AUTHOR"]
		dictionary = ibm_db.fetch_assoc(stmt)





