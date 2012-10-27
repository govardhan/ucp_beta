from dbpool import DBPool
from genutils import *
from uv_decorators import *
from config import UVConfig
import time
import re

@singleton
class Normalizer:
  def __init__(self):
    self.init()
  
  def reload(self):
    self.init()

  def init(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core") 
    self.noofrule, self.normalize_rules = DBPool().execute_query("select id, in_pattern, out_pattern, telco_id, channel, description from tb_number_normalizer order by id desc", self.db_name)

    logging.info("Normalized rules in search order top to bottom")
    logging.info("id	in_pattern	out_pattern	telco_id	channel		desc")
    logging.info("-" * 70)
    for l_row in self.normalize_rules:
      logging.info("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(l_row['id'], l_row['in_pattern'], l_row['out_pattern'], l_row['telco_id'], l_row['channel'], l_row['description']))

  def normalize(self, p_msisdn, p_telco_id = ".*", p_channel = ".*"):
    logging.debug("params - p_msisdn {0}, p_telco_id {1}, p_channel {2}".format(p_msisdn, p_telco_id, p_channel))
    for l_row in self.normalize_rules:
      if( (None != re.match(l_row['in_pattern'], p_msisdn)) and (None != re.match(l_row['telco_id'], p_telco_id)) and (None != re.match(l_row['channel'], p_channel))  ):
        l_norm_msisdn = re.sub(l_row['in_pattern'], l_row['out_pattern'], p_msisdn)
        logging.info("Matchfound. p_msisdn = {0}, l_norm_msisdn = {1}, id = {2}, in_pattern = {3}, out_pattern = {4}, telco_id = {5}, channel = {6}, p_telco_id = {7}. p_channel = {8}".format(p_msisdn, l_norm_msisdn, l_row['id'], l_row['in_pattern'], l_row['out_pattern'], l_row['telco_id'], l_row['channel'], p_telco_id, p_channel) )
        return True, l_norm_msisdn

    #End of for loop. No match found. So return False
    logging.info("No normalizer match not found. p_msisdn = {0}, p_telco_id = {1}. p_channel = {2}".format(p_msisdn, p_telco_id, p_channel) )
    return False, p_msisdn

#Run unit tests
if __name__ == "__main__":
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")

  l_normalizer = Normalizer()
  l_found, l_result = l_normalizer.normalize("9886161856")
  l_found, l_result = l_normalizer.normalize("9886161856", p_telco_id = "91.*")


