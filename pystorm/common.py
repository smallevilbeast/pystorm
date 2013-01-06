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

import os
import cPickle
import fcntl
import hashlib

from .logger import newLogger
from .xdg import get_cache_dir

logger = newLogger("common")

def get_md5(string):                
    return hashlib.md5(string).hexdigest()

def get_state_file(url):
    return os.path.join(get_cache_dir(), get_md5(url))

def save_db(objs, fn):
    '''Save object to db file.'''
    
    f = open(fn + ".tmp", "wb")
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    cPickle.dump(objs, f, cPickle.HIGHEST_PROTOCOL)
    f.close()
    try:
        os.rename(fn + ".tmp", fn)
    except:    
        pass
    
def load_db(fn):    
    '''Load object from db file.'''
    
    objs = None
    
    if os.path.exists(fn):
        f = open(fn, "rb")
        try:
            objs = cPickle.load(f)
        except:    
            logger.logexception("%s is not a valid database.", fn)
            try:
                os.unlink(fn)
            except: pass    
            
            objs = None
        f.close()    
    return objs    
