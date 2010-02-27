#!/usr/bin/env python

import main

def assignment2():
  if len(sys.argv) is not 3 or sys.argv[2][sys.argv[2].rfind(".")+1:] != "cfg":
    print "[*] Usage: python main.py [ddl] [config.cfg] - see README for config format"
    sys.exit()    
    # read in config sections
    node1 = config('node1', sys.argv[2])
    db1 = ibm_db.pconnect(node1['hostname'], node1['username'],node1['passwd'])
    print_table(db1, '*', 'SAMPLE')
    
if __name__ == "__main__":
    assignment2()
