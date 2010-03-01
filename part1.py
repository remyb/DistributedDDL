#!/usr/bin/python

# Assignment 1 - Part 1 and 2

import sys, ibm_db
from threading import Thread
from main import *

# Check for Proper Usage
if len(sys.argv) is not 3 or sys.argv[2][sys.argv[2].rfind(".")+1:] != "cfg":
	print "[*] Usage: python main.py [ddl] [config.cfg] - see README for config format"
	sys.exit() 
   
# read in config sections
node1 = config_extract(sys.argv[2], 'node1')
node2 = config_extract(sys.argv[2], 'node2')
catalog = config_extract(sys.argv[2], 'catalog')
	
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
			insert_catalog_row(query, cat, node1, 1)
		elif node is db2:
			insert_catalog_row(query, cat, node2, 2)

# close persistant connections
for node in nodes:
	ibm_db.close(node)
ibm_db.close(cat)
