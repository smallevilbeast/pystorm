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

PROGRAM_NAME = "pystorm"

homedir = os.path.expanduser("~")
lastdir = homedir

data_home = os.environ.get('XDG_DATA_HOME') or \
            os.path.join(homedir, '.local', 'share')

config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.join(homedir, '.config')

cache_home = os.environ.get('XDG_CACHE_HOME') or \
            os.path.join(homedir, '.cache')

data_home = os.path.join(data_home, PROGRAM_NAME)
config_home = os.path.join(config_home, PROGRAM_NAME)
cache_home = os.path.join(cache_home, PROGRAM_NAME)

program_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

local_hack = False
# Detect if Exaile is not installed.
if os.path.exists(os.path.join(program_dir, 'setup.py')):
    local_hack = True

def get_config_dir():
    return config_home

def get_data_dir():
    return data_home

def get_cache_dir():
    return cache_home

def _get_path(basedirs, *subpath_elements, **kwargs):
    check_exists = kwargs.get("check_exists", True)
    subpath = os.path.join(*subpath_elements)
    for d in basedirs:
        path = os.path.join(d, subpath)
        if not check_exists or os.path.exists(path):
            return path
    return None

def get_last_dir():
    return lastdir

def get_specify_cache_dir(*subpath):
    path = os.path.join(get_cache_dir(), *subpath)
    if not os.path.exists(path):
        os.makedirs(path)
    return path    

def make_missing_dirs():
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    if not os.path.exists(config_home):
        os.makedirs(config_home)
    if not os.path.exists(cache_home):
        os.makedirs(cache_home)
        
make_missing_dirs()        
