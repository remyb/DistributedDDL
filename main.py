import ibm_db, ConfigParser

# connect to database
conn = ibm_db.connect('SAMPLE','db2inst1','x') # insert here with your connection info
db1 = ibm_db.connect('ASSIGN01','db2inst1','x') # insert here with your connection info
db2 = ibm_db.connect('ASSIGN02','db2inst1','x') # insert here with your connection info

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
  else:
    print "Successfully Created Table!"


def drop_table(db):
  try:
    stmt = ibm_db.exec_immediate(db,"DROP TABLE BOOKS")
  except:
    print "There may be nothing to drop! \n-----------\n:", ibm_db.stmt_errormsg()
  else:
    print "Successfully Dropped Table!"
    

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

client_print(db1)
# for each node in config connect to that node and execute query in threads
print "The server is: ",config('section')['server'],":",config('section')['port']
print_table()
#create_table(db1)  # going to thread these
#create_table(db2)
#drop_table()
ibm_db.close(conn)

