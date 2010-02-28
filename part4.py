#!/usr/bin/python

from main import *
import sys
from ConfigExtractor import ConfigExtractor

if len(sys.argv) is not 3:
  print "[*] Usage: python part4.py [temp.cfg] [csvfile]"
  print sys.argv[0],sys.argv[1]
  print sys.argv.len
  sys.exit()

# load CSV
csv_contents = loadCSV(sys.argv[2])

# Get Catalog and Parition Sections
configuration = ConfigExtractor(sys.argv[1])
catalog = configuration.getSection('catalog')
#partition = configuration.getSection('partition')

# Make persistant catalog connection
conn = ibm_db.pconnect(catalog['hostname'], catalog['username'],catalog['passwd'])

# Get a list of nodes that contain table name
tablename = "BOOKST"
nodes = get_nodes(conn, tablename)
print "Number of Nodes: ",len(nodes)

# Create a list of connected node objects
connections = []
for node in nodes:
  print node
  connections.append(ibm_db.pconnect(node[0], node[1],node[2]))

method = partition['column'].lower()
method_types = ('notpartition', 'range', 'hash')
if method == method_types[0]:
  
# Partition these nodes and send to specific connection
#column = partition['column'].lower()
column = 'title'
for row in csv_contents:
  if column == 'isbn':
    print row[0]
  elif column == 'title':
    print row[1]
  elif column == 'author':
    print row[2]

# Send dtables row to catalog
#sql = "INSERT INTO DTABLES VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s');" % tablename, driver, url, user, passwd, partmtd, nodeid, partcol, partparam1, partparam2)
#exec_query(conn, sql);


  




