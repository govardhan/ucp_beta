from dbpool import DBPool
from genutils import *
from uv_decorators import *
from config import UVConfig
import time
import re

@singleton
class UVTelcoProfile:
  def __init__(self):
    self.init()
  
  def reload(self):
    self.init()

  def init(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core") 
    self.rowcount, self.telco_profiles = DBPool().execute_query("select id, telco_id, lang, obd_cic_group, mt_sms_type, mo_sms_type, num_resol_type, port_in_out, event_bill_type, subs_bill_type, renew_bill_type, unsub_bill_type from tb_telco_profile order by id desc", self.db_name)

    logging.info("Telco profiles in search order top to bottom")
    logging.info("-" * 70)
    for l_row in self.telco_profiles:
      logging.info("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}".format(l_row['id'], l_row['telco_id'], l_row['lang'], l_row['obd_cic_group'], l_row['mt_sms_type'], l_row['mo_sms_type'], l_row['num_resol_type'], l_row['port_in_out'], l_row['event_bill_type'], l_row['subs_bill_type'], l_row['renew_bill_type'], l_row['unsub_bill_type']))

  def get_lang(self, p_telco_id = ".*", p_lang_opt = 1):
    logging.debug("params - p_telco_id {0} p_lang_opt {1} ".format(p_telco_id, p_lang_opt))
    l_lang = "eng"
    for l_row in self.telco_profiles:
      if( (None != re.match(l_row['telco_id'], p_telco_id)) ):
        for l_lang_opt in l_row['lang'].split(","):
          if( int(p_lang_opt) == int(l_lang_opt.split("=")[0]) ):
            l_lang = l_lang_opt.split("=")[1]  

        logging.info("Matchfound for p_telco_id {0}, p_lang_opt {1}. id = {2}, telco_id = {3}, lang = {4}, l_lang = {5} ".format(p_telco_id, p_lang_opt, l_row['id'], l_row['telco_id'], l_row['lang'], l_lang) )
        return True, l_lang

    #End of for loop. No match found. So return False
    logging.error("No default language found for  p_telco_id {0} p_lang_opt {1} . Using english".format(p_telco_id, p_lang_opt) )
    return False, l_lang


  def get_profile_val(self, p_profile_key, p_telco_id = ".*"):
    logging.debug("params - p_telco_id {0}, p_profile_key {1}".format(p_telco_id, p_profile_key))
    for l_row in self.telco_profiles:
      if( (None != re.match(l_row['telco_id'], p_telco_id)) ):
        logging.debug("Matchfound for p_telco_id {0}, p_profile_key {1} p_profile_val {2}".format(p_telco_id, p_profile_key, l_row[p_profile_key]))
        return True, l_row[p_profile_key]
      else:
        logging.warn("No Match found for p_telco_id {0}, p_profile_key {1}".format(p_telco_id, p_profile_key))
        return False, None

  def get_obd_cic_group(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "obd_cic_group", p_telco_id)

  def get_mt_sms_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "mt_sms_type", p_telco_id)

  def get_mo_sms_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "mo_sms_type", p_telco_id)

  def get_num_resol_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "num_resol_type", p_telco_id)

  def get_port_in_out(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "port_in_out", p_telco_id)

  def get_event_bill_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "event_bill_type", p_telco_id)

  def get_subs_bill_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "subs_bill_type", p_telco_id)

  def get_renew_bill_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "renew_bill_type", p_telco_id)

  def get_unsub_bill_type(self, p_telco_id = ".*"):
    return self.get_profile_val(self, "unsub_bill_type", p_telco_id)


#Run unit tests
if __name__ == "__main__":
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")

  l_telco_profile = UVTelcoProfile()
  l_found, l_result = l_telco_profile.get_lang("91.BH")
  l_found, l_result = l_telco_profile.get_lang("966.STC")


