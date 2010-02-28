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
#print "Loading...",csv_contents

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
  connections.append(node)
  


  




