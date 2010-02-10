#!/usr/bin/python

import ibm_db, ConfigParser
from threading import Thread

# read config and parse
def config(section):
  config = ConfigParser.RawConfigParser()
  config.read('test.cfg')
  dict = {}
  options = config.options(section)
  for option in options:
    try:
			dict[option] = config.get(section, option)
			if dict[option] == -1:
				DebugPrint("skip: %s" % option)
    except:
    	print("exception on %s!" % option)
    	dict[option] = None
  return dict

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


def create_table(db):
  try:
    stmt = ibm_db.exec_immediate(db,"CREATE TABLE BOOKS(isbn char(14), title char(80), price decimal);")
  except:
    print "The table probably already exists: \n----------\n" , ibm_db.stmt_errormsg()
    return False
  else:
    print "Successfully Created Table!"


def drop_table(db):
  try:
    stmt = ibm_db.exec_immediate(db,"DROP TABLE BOOKS")
  except:
    print "There may be nothing to drop! \n-----------\n:", ibm_db.stmt_errormsg()
  else:
    print "Successfully Dropped Table!"

# execute query
def exec_query(db, query):
  try:
    ibm_db.exec_immediate(db,query)
  except:
    print "the query could not be completed:\n",query 
  else:
    print "the query was successful:\n",query 

# works on SAMPLE database created with db2sampl program
def print_table():
  sql = "SELECT * FROM DEPARTMENT"
  stmt = ibm_db.exec_immediate(conn,sql)
  dictionary = ibm_db.fetch_assoc(stmt)
  while dictionary != False:
    print '==================='
    print "Department #: ",dictionary["DEPTNO"]
    print "Department Name: ",dictionary["DEPTNAME"]
    print "Department Location: ",dictionary["LOCATION"]
    dictionary = ibm_db.fetch_assoc(stmt)

#client_print(db1)


node1 = config('node1')
node2 = config('node2')
db1 = ibm_db.connect(node1['hostname'], node1['username'],node1['passwd'])
db2 = ibm_db.connect(node2['hostname'], node2['username'],node2['passwd'])

nodes = [db1,db2]
querys = ["CREATE TABLE BOOKS(isbn char(14), title char(80), price decimal);","DROP TABLE BOOKS"]

# foreach db execute the DDL's
for query in querys:
  for node in nodes:  
    Thread(target=exec_query,args=(node,query,)).start()
  
for node in nodes:
  ibm_db.close(node)
  
#try:
#except Exception, errtxt:
#print errtxt

#thread.start_new_thread(drop_table,(db2))

#create_table(db1)  # going to thread these
#create_table(db2)


#drop_table()
#print_table()
#ibm_db.close(conn)

