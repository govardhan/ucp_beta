from dbpool import DBPool
from genutils import *
from uv_decorators import *
from config import UVConfig
import time
import re

class UVUserProfileHandler:
  def __init__(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core")

  def create_profile(self, p_msisdn, p_lang, p_telco_id, p_user_name, p_user_type = "user", p_channel = "ivr", p_notify_pref = "sms"):
    logging.debug("params p_msisdn {0}, p_telco_id {1}, p_user_name {2}, p_user_type {3}, p_channel {4}, p_notify_pref {5}".format(p_msisdn, p_lang, p_telco_id, p_user_name, p_user_type, p_channel, p_notify_pref))
    self.rowcount, l_tmp = DBPool().execute_query("insert into tb_user_profile(msisdn, lang, telco_id, user_name, user_type, channel, notify_pref) values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(p_msisdn, p_lang, p_telco_id, p_user_name, p_user_type, p_channel, p_notify_pref), self.db_name)
    if(self.rowcount):
      logging.info("user profile created for {0} - p_telco_id {1}, p_user_name {2}, p_user_type {3}, p_channel {4}, p_notify_pref {5}".format(p_msisdn, p_lang, p_telco_id, p_user_name, p_user_type, p_channel, p_notify_pref))
      return True
    else:
      logging.error("failed to create user profile for 0} - p_telco_id {1}, p_user_name {2}, p_user_type {3}, p_channel {4}, p_notify_pref {5}".format(p_msisdn, p_lang, p_telco_id, p_user_name, p_user_type, p_channel, p_notify_pref))
      return False

  #TODO Improve efficiency while returning profile data
  def get_profile(self, p_msisdn):
    logging.debug("param p_msisdn {0}".format(p_msisdn))
    l_found, l_profile = DBPool().execute_query("select msisdn,lang, telco_id, status, user_type, created_ts, updated_ts, privacy, follower_count, following_count, user_name, blog_box_size, new_inbox_size, heard_inbox_size, save_inbox_size, fwd_inbox_size, blog_box_ttl, new_inbox_ttl, heard_inbox_ttl, save_inbox_ttl, fwd_inbox_ttl, notify_pref, email, display_name, password, location, channel, device_id, user_desc, profile_url, intro_audio_url, image_url, current_location, facebook_id, facebook_username, facebook_screenname, twitter_username, facebook_token, twitter_id, twitter_token, twitter_token_secret, twitter_screenname, block_list from tb_user_profile where msisdn = '{0}'".format(p_msisdn), self.db_name)
    if(l_found):
      logging.info("User profile found l_found {0}, profile {1}".format(l_found, l_profile))
      return True, l_profile;
    else:
      return False, None;

  #Write more API's to update user profile parameters


#Run unit tests
if __name__ == "__main__":
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")

  l_user_profile = UVUserProfileHandler()
  #l_user_profile.create_profile("919011223344", "arabic", "91.BH", "govi") 
  #l_user_profile.create_profile("919011226677", "hin", "91.BH", "ammar", "celeb", "cli") 

  l_found, l_profile = l_user_profile.get_profile("919011223345") 
  if(True == l_found):
    logging.info("Profile found for l_profile {0}".format(l_profile[0]['msisdn']))
  else:
    logging.info("Profile not found. Creating now")
    l_user_profile.create_profile("919011223345", "arabic", "91.BH", "govi5") 

