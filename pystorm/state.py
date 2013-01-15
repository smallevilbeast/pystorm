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
from threading import Lock

from .logger import Logger
from . import common

class ConnectionState(Logger):
    
    def __init__(self, n_conn, filesize):
        self.n_conn = n_conn
        self.filesize = filesize
        self.progress = [0 for i in range(n_conn)]
        self.elapsed_time = 0
        self.chunks = [(filesize / n_conn) for i in range(n_conn)]
        self.chunks[0] += filesize % n_conn
        self.save_lock = Lock()
        
        self.save_objs = common.Storage()

    def download_sofar(self):
        dwnld_sofar = 0
        for rec in self.progress:
            dwnld_sofar += rec
        return dwnld_sofar

    def update_time_taken(self, elapsed_time):
        self.elapsed_time += elapsed_time

    def update_data_downloaded(self, fetch_size, conn_id):
        self.progress[conn_id] += fetch_size

    def resume_state(self, state_file, output_file):
        if not os.path.isfile(output_file):
            return 
        saved_obj = common.load_db(state_file)
        if not saved_obj:
            return 
        
        for p in "n_conn filesize progress chunks elapsed_time".split():
            if not hasattr(saved_obj, p):
                return 
        
        self.n_conn = saved_obj.n_conn
        self.filesize = saved_obj.filesize
        self.progress = saved_obj.progress
        self.chunks = saved_obj.chunks
        self.elapsed_time = saved_obj.elapsed_time
        
    def _save_state(self):    
        self.save_objs.n_conn = self.n_conn
        self.save_objs.filesize = self.filesize
        self.save_objs.progress = self.progress
        self.save_objs.chunks = self.chunks
        self.save_objs.elapsed_time = self.elapsed_time

    def save_state(self, state_file):
        #out_fd will be closed after save_state() is completed
        #to ensure that state is written onto the disk
        self.save_lock.acquire()
        self._save_state()
        common.save_db(self.save_objs, state_file)
        self.save_lock.release()
