import ibm_db

# connect to database
conn = ibm_db.connect() # insert here with your connection info

#show stats on database
def client_print(): 
  client = ibm_db.client_info(conn)
  print "DRIVER_NAME: string(%d) \"%s\"" % (len(client.DRIVER_NAME), client.DRIVER_NAME)
  print "DRIVER_VER: string(%d) \"%s\"" % (len(client.DRIVER_VER), client.DRIVER_VER)
  print "DATA_SOURCE_NAME: string(%d) \"%s\"" % (len(client.DATA_SOURCE_NAME), client.DATA_SOURCE_NAME)
  print "DRIVER_ODBC_VER: string(%d) \"%s\"" % (len(client.DRIVER_ODBC_VER), client.DRIVER_ODBC_VER)
  print "ODBC_VER: string(%d) \"%s\"" % (len(client.ODBC_VER), client.ODBC_VER)
  print "ODBC_SQL_CONFORMANCE: string(%d) \"%s\"" % (len(client.ODBC_SQL_CONFORMANCE),      client.ODBC_SQL_CONFORMANCE)
  print "APPL_CODEPAGE: int(%s)" % client.APPL_CODEPAGE
  print "CONN_CODEPAGE: int(%s)" % client.CONN_CODEPAGE

# Assumes the table does not exist
def create_table():
  try:
    stmt = ibm_db.exec_immediate(db,"CREATE TABLE BOOKS(isbn char(14), title char(80), price decimal);")
  except:
    print "The table probably already exists: " , ibm_db.stmt_errormsg()
  else:
    print "Successfully Created Table!"
    
def drop_table():
  try:
    stmt = ibm_db.exec_immediate(db,"DROP TABLE BOOKS")
  except:
    print "There may be nothing to drop! :", ibm_db.stmt_errormsg()
  else:
    print "Successfully Dropped Table!"
    


client_print()
#create_table()
#drop_table()
ibm_db.close(conn)

