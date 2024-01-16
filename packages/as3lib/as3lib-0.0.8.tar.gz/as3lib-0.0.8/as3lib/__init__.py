from . import configmodule, initconfig
if configmodule.initdone == False:
   initconfig.initconfig()
from . import *