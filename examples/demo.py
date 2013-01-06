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

import gobject
gobject.threads_init()

import glib

from pystorm.services import FetchService
from pystorm.tasks import TaskObject

fetch_service = FetchService(5)
fetch_service.start()

task_list = []
for i in ["http://packages.linuxdeepin.com/deepin/pool/main/d/deepin-emacs/deepin-emacs_1.1-1_all.deb", 
          "http://packages.linuxdeepin.com/deepin/pool/main/d/deepin-unity-greeter/deepin-unity-greeter_0.2.9-1_amd64.deb"]:
    
    task_list.append(TaskObject(i))
    
fetch_service.add_missions(task_list)    
main_loop = glib.MainLoop()
main_loop.run()



