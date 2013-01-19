#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re

levelno = logging.DEBUG
def setLevelNo(n):
    global levelno
    levelno = ( 100 - (n * 10) )

logging.addLevelName(100, "DEPRECATED")
console_format = '%(levelname)-8s %(name)-30s %(message)s'
logging.basicConfig(level=levelno, format=console_format, datafmt="%H:%M:%S")


def objaddr(obj):
    string = object.__repr__(obj)
    m = re.search("at (0x\w+)",string)
    if m: return  m.group(1)[2:]
    return "       "


class Logger(object):

    def set_logname(self, name):
        self.__logname = name

    def get_logname(self):
        if hasattr(self,"__logname") and self.__logname :
            return self.__logname
        else:
            return "%s.%s"%(self.__module__,self.__class__.__name__)

    def logdebug(self, msg, *args, **kwargs): 
        mylogger = logging.getLogger(self.get_logname())
        mylogger.debug(msg, *args, **kwargs)

    def loginfo(self, msg, *args, **kwargs): 
        mylogger = logging.getLogger(self.get_logname())
        mylogger.info(msg, *args, **kwargs)

    def logwarn(self, msg, *args, **kwargs): 
        mylogger = logging.getLogger(self.get_logname())
        mylogger.warn(msg, *args, **kwargs)

    def logerror(self, msg, *args, **kwargs): 
        mylogger = logging.getLogger(self.get_logname())
        mylogger.error(msg, *args, **kwargs)

    def logcritical(self, msg, *args, **kwargs): 
        mylogger = logging.getLogger(self.get_logname())
        mylogger.critical(msg, *args, **kwargs)

    def logexception(self, msg, *args, **kwargs):
        mylogger = logging.getLogger(self.get_logname())
        mylogger.exception(msg, *args, **kwargs)

    def logdeprecated(self, msg, *args, **kwargs):
        mylogger = logging.getLogger(self.get_logname())
        mylogger.log(100,msg, *args, **kwargs)

def newLogger(name):
    l = Logger()
    l.set_logname(name)
    return l

