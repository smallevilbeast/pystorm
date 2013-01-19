#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
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

import ssl
import socket
import httplib
import urllib2

class VerifiedHTTPSConnection(httplib.HTTPSConnection):
    def connect(self):
        # overrides the version in httplib so that we do
        #    certificate verification
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        # wrap the socket using verification with the root
        #    certs in trusted_root_certs
        self.sock = ssl.wrap_socket(sock,
                                    self.key_file,
                                    self.cert_file,
                                    cert_reqs=ssl.CERT_REQUIRED,
                                    ca_certs="trusted_root_certs")
        
        
        
# wraps https connections with ssl certificate verification
class VerifiedHTTPSHandler(urllib2.HTTPSHandler):
    '''
    >>> https_handler = VerifiedHTTPSHandler()
    >>> url_opener = urllib2.build_opener(https_handler)
    >>> handle = url_opener.open('https://www.example.com')
    >>> response = handle.readlines()
    >>> handle.close()    
    
    '''
    def __init__(self, connection_class = VerifiedHTTPSConnection):
        self.specialized_conn_class = connection_class
        urllib2.HTTPSHandler.__init__(self)
        
    def https_open(self, req):
        return self.do_open(self.specialized_conn_class, req)
