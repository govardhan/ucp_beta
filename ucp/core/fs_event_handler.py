#!/usr/bin/env python

import SocketServer
import logging
from genutils import *
from ESL import *


def handle_setloglevel_signal(level):
  #logging.disable(level - 1);
  #logging.disable(0) #this makes all log levels will be printed
  pass

class ESLRequestHandler(SocketServer.BaseRequestHandler ):
  def setup(self):
    logging.info("New incoming call. client address %s ", self.client_address)

    fd = self.request.fileno()
    logging.info("socket descriptor is %d", fd)

    con = ESLconnection(fd)
    logging.info("ESL connection status %s", con.connected())
    if con.connected():
      info = con.getInfo()

      uuid = info.getHeader("unique-id")
      logging.info("callinfo: uuid %s ", uuid)
      con.execute("answer", "", uuid)
      #con.execute("playback", "/home/uvadmin/ucp/conf/prompts/welcome2vtweet.wav", uuid);
      con.execute("playback", "/home/freeswitch/vtweet/prompts/welcome2vtweet.wav", uuid);
    else:
      logging.error("Could not get ESL connection for socket descriptor %d", fd)


def main():
  init_logging("voiceapp.log")
  logging.info("Starting application uvas")
  #server host is a tuple ('host', port)
  sock_server = SocketServer.ThreadingTCPServer(('', 8040), ESLRequestHandler)
  sock_server.serve_forever()

if __name__=='__main__':
  main()
