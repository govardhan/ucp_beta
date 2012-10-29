from dbpool import DBPool
from genutils import *
from uv_decorators import *
from config import UVConfig
import time
import re

@singleton
class UVAppManager:
  def __init__(self):
    self.db_name = UVConfig().get_config_value("database","db_name.core") 

  def handleService(p_uuid, p_src_norm_num, p_dst_srvc_norm_num, p_src_telcoId, p_dst_telcoId, p_service_id):
    logging.debug("params - p_uuid {0}, p_src_norm_num {1}, p_dst_srvc_norm_num {3}, p_src_telcoId {4}, p_dst_telcoId {5}, p_service_id {6}".format(p_uuid, p_src_norm_num, p_dst_srvc_norm_num, p_src_telcoId, p_dst_telcoId, p_service_id))
    if("VSMS_POST" == p_service_id):
      VSMSApp().execute(p_uuid, p_src_norm_num, p_dst_srvc_norm_num, p_src_telcoId, p_dst_telcoId)
    else:
      logging.error("{0} service id {1} not found".format(p_uuid, p_service_id))
   
