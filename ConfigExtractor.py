#!/usr/bin/python
import ConfigParser,sys

# Parses and stores the cluster configuration
class ConfigExtractor:
  def __init__(self, configfile):
    self.settings = configfile
    self.items = {}
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.settings)
  
  # Returns a dictionary of a specific config section
  def getSection(self, section):
    try:
      options = self.config.options(section)
    except:
      print "[*] The file is not in the correct format, please consult readme"
      sys.exit()
    for option in options:
      try:
        self.items[option] = self.config.get(section, option)
        if self.items[option] == -1:
          DebugPrint("skip: %s" % option)
      except:
        print("exception on %s!" % option)
        self.items[option] = None
    return self.items
    
if __name__ == "__main__":
  # run some unit test
  config = ConfigExtractor(sys.argv[1])
  node1 = config.getSection('node1')
  print "Username: " + node1['username']
  print "Password: " + node1['passwd']
