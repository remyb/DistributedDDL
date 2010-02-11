#!/usr/bin/python

#Remy Baumgarten
#Kevin Chiogioji


import ibm_db, ConfigParser,time, sys
from threading import Thread

# read config and parse
def config(section, settings):
  config = ConfigParser.RawConfigParser()
  config.read(settings)
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


# execute query
def exec_query(db, query):
  try:
    ibm_db.exec_immediate(db,query)
  except:
    print "[*] The transaction could not be completed:", query #ibm_db.stmt_errormsg()
  else:
    print "[*] Transaction complete: ",query

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

# check to see if dtables in CATALOG exists, if not, create it
def create_catalog(cat, catalog):
  try:
    ibm_db.exec_immediate(cat,"CREATE TABLE "+catalog['table'])
  except:
    print "[*] NOTICE catalog table exists"

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
    " nodepasswd, partmtd, partparam1, partparam2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,);" % (tableName.rstrip(";"), node_conf["driver"], node_conf ["hostname"], node_conf["username"], node_conf["passwd"], "NULL", "NULL", "NULL")  
  print cat_row

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

###############################################################################

# Check that two file names were entered
if len(sys.argv) is not 3:
  print "[*] Usage: python main.py [ddl] [config.cfg] - see README for config format"
  sys.exit()    

# read in config sections
node1 = config('node1', sys.argv[2])
node2 = config('node2', sys.argv[2])
catalog = config('catalog', sys.argv[2])

# make persistant connections to distributed databases
db1 = ibm_db.pconnect(node1['hostname'], node1['username'],node1['passwd'])
db2 = ibm_db.pconnect(node2['hostname'], node2['username'],node2['passwd'])
cat = ibm_db.pconnect(catalog['hostname'], catalog['username'],catalog['passwd'])

# create catalog if doesn't exist
create_catalog(cat,catalog)

# list of nodes and queries to iterate through
nodes = [db1,db2]
querys = readDDL(sys.argv[1])

# foreach DDL, execute queries on all nodes
for query in querys:
  for node in nodes:  
    Thread(target=exec_query,args=(node,query,)).start()
    if node is db1:
      insert_catalog_row(query, cat, node1)
    elif node is db2:
      insert_catalog_row(query, cat, node2)  
 # time.sleep(4) # give time to rest before dropping a table not yet created
 
  
# close persistant connections
for node in nodes:
  ibm_db.close(node)
ibm_db.close(cat)

