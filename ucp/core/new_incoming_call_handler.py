#!/usr/bin/env python

import logging
import redis

from genutils import *
from cache_server import UVCache 
from config import UVConfig
from number_normalize import UVNormalizer
from number_telco_resolution import UVNumberTelcoResolution
from service_finder import *

class NewIncomingCallHandler:
  def __init__(self, p_uuid, p_src_num, p_dst_num):
    self.uuid = p_uuid
    self.src_num = p_src_num 
    self.dst_num = p_dst_num

  def update_stats_on_newcall(self):
    UVCache().incr( UVConfig().get_config_value("stats","active_incoming_call_counter") )

    UVCache().incr( UVConfig().get_config_value("stats","incoming_call_counter") )

    l_active_incoming_call_counter = int(UVCache().get( UVConfig().get_config_value("stats","active_incoming_call_counter") ))
    if( l_active_incoming_call_counter > int(UVCache().get( UVConfig().get_config_value("stats","max_active_incoming_calls") )) ):
      UVCache().set( UVConfig().get_config_value("stats","max_active_incoming_calls"), l_active_incoming_call_counter )

     
  def process_newcall(self):
    #updates stats, normalize src & dst num, resolve src & dst num, find service id and handover to service app 
    #TODO - get src telcoid from channel group
    
    self.update_stats_on_newcall()
    l_src_norm_status, self.src_norm_num = UVNormalizer().normalize(self.src_num)
    l_dst_norm_status, self.dst_norm_num = UVNormalizer().normalize(self.dst_num)


    #TODO what if src & dst numbers telcoid not found? Assign default telcoid for src num and log CRITICAL error.
    l_src_telcoid_found, self.src_telcoId, l_src_flags = UVNumberTelcoResolution().get_telco_id(self.src_norm_num)

    #TODO have configurable value
    self.channel = "ivr"
    l_srvc_found, self.service_id, self.dst_srvc_num = UVServiceMap().get_service_id(self.dst_norm_num, self.src_telcoId, self.channel);

    l_dst_srvc_norm_status, self.dst_srvc_norm_num = UVNormalizer().normalize(self.dst_srvc_num)
    l_dst_telcoid_found, self.dst_telcoId, l_src_flags = UVNumberTelcoResolution().get_telco_id(self.dst_srvc_norm_num)
   
    #Fetch user profile if exists. Create if not exists
    l_found, l_profile = UVUserProfileHandler().get_profile(self.src_norm_num)
    if(False == l_found):
      UVUserProfileHandler().create_profile(self.src_norm_num, UVTelcoProfile().get_lang(self.src_telcoId), self.src_telcoId, elf.src_norm_num)
      
    UVAppManager().handleService(self.uuid, self.src_norm_num, self.dst_srvc_norm_num, self.src_telcoId, self.dst_telcoId, self.service_id);

#Run unit tests
if __name__ == "__main__":
  init_logging("voiceapp.log")
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")

  NewIncomingCallHandler('1234567890', '9886161856', '*9988776655').process_newcall()
  NewIncomingCallHandler('1234567891', '9000001111', '*9988776655').process_newcall()
    
