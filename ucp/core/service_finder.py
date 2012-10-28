from dbpool import DBPool
from genutils import *
from uv_decorators import *
from config import UVConfig
import time
import re

@singleton
class UVServices:
  def __init__(self):
    self.init()
  def reload():
    self.init()

  def init(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core")
    self.rowcount, self.services = DBPool().execute_query("select id, service_id, service_name, service_group, remarks from tb_services order by id", self.db_name)
    logging.info("id     service_id       service_name      service_group        remarks")
    logging.info("-" * 70)
    for l_row in self.services:
      logging.info("{0}\t{1}\t{2}\t{3}\t{4}".format(l_row['id'], l_row['service_id'], l_row['service_name'], l_row['service_group'], l_row['remarks']))
    
  def get_service_name_group(self, p_service_id):
    for l_srvc_row in self.services:
      if( l_srvc_row['service_id'] == p_service_id):
        return l_srvc_row['service_name'], l_srvc_row['service_group']
      else:
        return None, None

  def get_service_id_group(self, p_service_name):
    for l_srvc_row in self.services:
      if( l_srvc_row['service_name'] == p_service_name):
        return l_srvc_row['service_id'], l_srvc_row['service_group']
      else:
        return None, None


@singleton
class UVServiceMap:
  def __init__(self):
    self.init()

  def reload(self):
    self.init()

  def init(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core")
    self.rowcount, self.srvc_map = DBPool().execute_query("select id, in_pattern, out_pattern, telco_id, channel, service_id, remarks from tb_service_map order by id desc", self.db_name)
    logging.info("Service map list in search order top to bottom")
    logging.info("id    in_pattern      out_pattern     telco_id        channel        service_id	 remarks")
    logging.info("-" * 70)
    for l_row in self.srvc_map:
      logging.info("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(l_row['id'], l_row['in_pattern'], l_row['out_pattern'], l_row['telco_id'], l_row['channel'], l_row['service_id'], l_row['remarks']))


  def get_service_id(self, p_msisdn, p_telco_id = ".*", p_channel = ".*"):
    logging.debug("params - p_msisdn {0}, p_telco_id {1}, p_channel {2}".format(p_msisdn, p_telco_id, p_channel))
    for l_row in self.srvc_map:
      if( (None != re.match(l_row['in_pattern'], p_msisdn)) and (None != re.match(l_row['telco_id'], p_telco_id)) and (None != re.match(l_row['channel'], p_channel))  ):
        l_service_id = l_row['service_id']
        l_out_num = re.sub(l_row['in_pattern'], l_row['out_pattern'], p_msisdn)
        logging.info("Matchfound. p_msisdn = {0}, l_service_id = {1}, id = {2}, in_pattern = {3}, out_pattern = {4}, telco_id = {5}, channel = {6}, p_telco_id = {7}. p_channel = {8}l_out_num = {9}".format(p_msisdn, l_service_id, l_row['id'], l_row['in_pattern'], l_row['out_pattern'], l_row['telco_id'], l_row['channel'], p_telco_id, p_channel, l_out_num) )
        return True, l_service_id, l_out_num
    #End of for loop. No match found. So return False
    logging.error("No service found for p_msisdn = {0}, p_telco_id = {1}. p_channel = {2}".format(p_msisdn, p_telco_id, p_channel) )
    return False, None, None


@singleton
class UVServiceProfile:
  def __init__(self):
    self.init()

  def reload(self):
    self.init()

  def init(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core")    
    self.rowcount, self.srvc_profiles = DBPool().execute_query("select id, service_id, profile_key, profile_value, remarks from tb_service_profile order by id", self.db_name)
    logging.info("{0} Service profiles found".format(self.rowcount)) 
    logging.info("id    service_id      profile_key     profile_value     remarks")
    logging.info("-" * 70)
    for l_row in self.srvc_profiles:
      logging.info("{0}\t{1}\t{2}\t{3}\t{4}".format(l_row['id'], l_row['service_id'], l_row['profile_key'], l_row['profile_value'], l_row['remarks']))

  def get_service_profile_value(self, p_service_id, p_profile_key):
    logging.debug("params - p_service_id {0}, p_profile_key {1}".format(p_service_id, p_profile_key))
    for l_row in self.srvc_profiles:
      if( (p_service_id == l_row['service_id']) and (p_profile_key == l_row['profile_key']) ):
        l_profile_val = l_row['profile_value']
        logging.info("Service profile value for p_service_id {0}, p_profile_key {1} = {2}".format(p_service_id, p_profile_key, l_profile_val))
        return True, l_profile_val
    logging.error("No service profile value found for p_service_id {0}, p_profile_key {1}".format(p_service_id, p_profile_key))
    return False, None



#Run unit tests
if __name__ == "__main__":
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")

  l_services = UVServices()
  logging.debug("service & groupname - {0}".format(l_services.get_service_name_group('VSMS_POST')))

  l_service_map = UVServiceMap()
  logging.debug("service_id - {0}".format(l_service_map.get_service_id("*9886161856", p_telco_id = "91.*")))

  l_service_profiles = UVServiceProfile()
  logging.debug("service profile value - {0}".format(l_service_profiles.get_service_profile_value('VSMS_POST', 'MAX_RECORD_DURATION')))
  logging.debug("service profile value - {0}".format(l_service_profiles.get_service_profile_value('DEFAULT', 'MAX_POST_DURATION')))

