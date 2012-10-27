from ConfigParser import SafeConfigParser
import os.path
import codecs
import logging
from genutils import *
from uv_decorators import *

@singleton
class UVConfig:
  def __init__(self):
    self.m_initialized = 0

  def init(self, p_filename):
    self.conf_filename = p_filename
    try:
      assert (len(self.conf_filename) != 0 and os.path.isfile(self.conf_filename) ) , "config file {0} is not valid".format(self.conf_filename)
    except AssertionError:
      logging.exception("config file {0} is not valid".format(self.conf_filename))
      raise

    logging.info("config filename {0}".format(self.conf_filename)) 

    self.parser = SafeConfigParser()
    with codecs.open(self.conf_filename, 'r', encoding='utf-8') as file_des:
      self.parser.readfp(file_des)

    for section_name in self.parser.sections():
      logging.info("section {0}".format(section_name)) 
      for key, value in self.parser.items(section_name):
        logging.info("config key = {0}, value = {1}".format(key, value))
      logging.info("")

    self.m_initialized = 1


  def get_config_value(self, p_section_name, p_key):
    try:
      assert self.m_initialized == 1, "UVConfig class has not yet initialized with config file"
    except AssertionError:
      logging.exception("UVConfig class has not yet initialized with config file")
      raise
        
    if self.parser.has_option(p_section_name, p_key):
      return self.parser.get(p_section_name, p_key)
    else:
      logging.warn("Config section {0}, key {1} not found in config file {2}".format(p_section_name, p_key, self.conf_filename))      
      return None


if __name__ == "__main__":
  #conf = UVConfig("/root/ucp/ucp/conf/ucp.conf")
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")
  
  
  print "Start testing"
  print conf.get_config_value("core","logfile_name")
  print conf.get_config_value("database","db_user_name")
  print conf.get_config_value("database","logfile_path")
  print conf.get_config_value("monitor", "logfile_path")
  
