#!/usr/bin/env python

import sys
from main import *
from antlr import *
from threading import Thread

if len(sys.argv) is not 3:
  print "[*] Usage: python part3.py [temp.cfg] [sqlfile] - see README for config format"
  sys.exit()   
catalog = config_extract(sys.argv[1], 'catalog')
conn = ibm_db.pconnect(catalog['hostname'], catalog['username'],catalog['passwd'])
# get sql
sqllist =  open(sys.argv[2])
lines = sqllist.readlines()
nodelist = []
for query in lines:
  #get tablename
  query = query.rstrip()
  if query == ';':
    continue
  tablename = get_table(query)
  #get nodes where this table occurs
  print "\n[*]Nodes that contain: ", tablename, ":"
  nodes = get_nodes(conn, tablename)
  nodelist.append(nodes)

connections = []
# unwrap list of lists
for nodes in nodelist:
  for node in nodes:
    print node
    print "[*] Placing connections into a list..."
    print node[0],node[1],node[2]
    connections.append(ibm_db.pconnect(node[0], node[1],node[2]))
for query in lines: 
  print "processing this query: ", query
  for database in connections:
    Thread(target=print_results,args=(database,query,)).start()
  
  
  
