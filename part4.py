#!/usr/bin/python

from main import *
import sys
from ConfigExtractor import ConfigExtractor

if len(sys.argv) is not 3:
  print "[*] Usage: python part4.py [temp.cfg] [csvfile]"
  sys.exit()

# load CSV
csv_contents = loadCSV(sys.argv[2])

# Get Catalog and Parition Sections
catalog = config_extract(sys.argv[1], 'catalog')
partition = config_extract(sys.argv[1], 'partition')

# Get Node partition information if range is specified
if(partition['method']=="range"):
  part_info1 = config_extract(sys.argv[1], 'node1')
  part_info2 = config_extract(sys.argv[1], 'node2')

# Make persistant catalog connection
conn = ibm_db.pconnect(catalog['hostname'], catalog['username'],catalog['passwd'])

# Get a list of nodes that contain table name
nodes = get_nodes(conn, partition['tablename'])
print "[DEBUG] Number of Nodes: ",len(nodes)

# Create a list of connected node objects
connections = []
for node in nodes:
  print node
  connections.append(ibm_db.pconnect(node[1], node[2],node[3]))

for connection in connections:
  client_print(connection)

method = partition['method'].lower()
column = partition['column'].lower()
partmtd = ('notpartition', 'range', 'hash')

print "***************",node_id(connections[0], 1)

if method == partmtd[0]:
  # place all rows in all database tables
  print "place all rows in all tables..."
elif method == partmtd[1]:
  print "ranger rick"
  column = partition['column']
  for row in csv_contents:
    if column == 'age':
      if row[1] > part_info1["node1.param1"] and row[1] <= part_info1["node1.param2"]:
        print row[1] + " in partition 1"
        #sql = "INSERT INTO " + 
        exec_query(connections[0], query)
      elif row[1] > part_info2["node2.param1"] and row[1] <= part_info2["node2.param2"]:
        print row[1] + " in partition 2"  
        exec_query(connections[1], query) 
    elif method == partmtd[2]:
      print "hash method"
  for row in csv_contents:
    nodenum = (int(row[0])%int(partition["param1"]))+1 
    print nodenum
    if (nodenum==1):
      print row[0] + " in partition 1"
    elif (nodenum==2):
      print row[0] + " in partition 2"
else:
  print "failbot", method, partmtd[1]
  exec_query(connections[0], query)
  exec_query(connections[1], query)



# Send dtables row to catalog
#sql = "INSERT INTO DTABLES VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s');" % tablename, driver, url, user, passwd, partmtd, nodeid, partcol, partparam1, partparam2)
#exec_query(conn, sql);


  




