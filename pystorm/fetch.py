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
import sys
import time
import threading
import urllib2
import socket
import traceback

socket.setdefaulttimeout(120)         # 2 minutes

from .logger import Logger

std_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; '
        'en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,'
        'text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'Accept-Language': 'en-us,en;q=0.5',
}


class HTTPFetch(threading.Thread, Logger):

    def __init__(self, name, url, part_output_file, state_file,
                 start_offset, conn_state):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
        self.part_output_file = part_output_file
        self.state_file = state_file
        self.start_offset = start_offset
        self.conn_state = conn_state
        self.length = conn_state.chunks[name] - conn_state.progress[name]
        self.sleep_timer = 0
        self.need_to_quit = False
        self.need_to_sleep = False
        
    @staticmethod    
    def get_file_size(url):
        try:
            conn = urllib2.urlopen(url, timeout=10)
            size = int(conn.info().getheaders("Content-Length")[0])
            conn.close()
            return size
        
        except urllib2.HTTPError:
            return 0
        
        except urllib2.URLError:
            return 0
        
        except ValueError:
            return 0
        
        except socket.timeout:
            return 0
        
        except Exception:
            traceback.print_exc(file=sys.stdout)
            return 0

    def run(self):
        if self.length == 0:
            return
        
        self.logdebug("Running thread with %d-%d", self.start_offset, self.length)
        
        request = urllib2.Request(self.url, None)
        request.add_header('Range', 'bytes=%d-%d' % (self.start_offset,
                                                     self.start_offset + self.length))
        while True:
            
            try:
                data = urllib2.urlopen(request)
                
            except urllib2.URLError, u:
                self.logdebug("Connection %s: did not start with %s", self.name, u)
            else:
                break

        # Open the output file
        out_fd = os.open(self.part_output_file, os.O_WRONLY)
        os.lseek(out_fd, self.start_offset, os.SEEK_SET)

        block_size = 1024
        #indicates if connection timed out on a try
        while self.length > 0:
            if self.need_to_quit:
                return

            if self.need_to_sleep:
                time.sleep(self.sleep_timer)
                self.need_to_sleep = False

            if self.length >= block_size:
                fetch_size = block_size
            else:
                fetch_size = self.length
            try:
                data_block = data.read(fetch_size)
                
                if len(data_block) == 0:
                    self.logdebug( "Connection %s: [TESTING]: 0 sized block fetched.", self.name)
                    
                if len(data_block) != fetch_size:
                    self.logdebug("Connection %s: len(data_block) != fetch_size, but continuing anyway.", self.name)
                    self.run()
                    return
            except socket.timeout, s:
                self.logdebug("Connection %s timed out with %s", self.name, s)
                self.run()
                return
            else:
                retry = 0

            self.length -= fetch_size
            
            self.conn_state.update_data_downloaded(fetch_size, int(self.name))
            self.logdebug("Connection %s: Update data downloaded", self.name)
            
            os.write(out_fd, data_block)
            self.start_offset += len(data_block)
            self.logdebug("Connection %s: Save state", self.name)
            self.conn_state.save_state(self.state_file)
        os.close(out_fd)    
            
