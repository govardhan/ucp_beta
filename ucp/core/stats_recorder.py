#!/usr/bin/env python

import logging
import redis

from genutils import *
from cache_server import UVCache


class UVStatsRecorder:
  pass

#implement timer functionality
#flush stats in to databae & reset at regular interval - 5 mins, hourly & daily basis
