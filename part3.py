#!/usr/bin/env python

import sys
from main import *

def assignment2():
  #if len(sys.argv) is not 3 or sys.argv[2][sys.argv[2].rfind(".")+1:] != "cfg":
  #  print "[*] Usage: python main.py [ddl] [config.cfg] - see README for config format"
  #  sys.exit()   
  # read in config sections
  #node1 = config('node1', sys.argv[2])
  db1 = ibm_db.pconnect("SAMPLE", "db2inst1","ics421ass1")
  #exec_query(db1, "CREATE TABLE BOOKS (number (int), author (varchar), ;")
  print_table(db1, '*', 'EMPLOYEE') # in turns does SELECT * FROM EMPLOYEE
    
if __name__ == "__main__":
    assignment2()
