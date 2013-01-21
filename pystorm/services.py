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

import sys
import time
import threading
import traceback
import Queue
from contextlib import contextmanager 

class FetchService(threading.Thread):
    
    def __init__(self, concurrent_thread_num=5):
        threading.Thread.__init__(self)
        
        self.setDaemon(True)
        
        self.concurrent_thread_num = concurrent_thread_num
        
        self.active_mission_list = []
        self.wait_mission_list = []
        self.mission_result_list = []
        
        self.thread_sync_lock = threading.Lock()
        self.mission_lock = Queue.Queue()
                
    def run(self):    
        while True:
            result = self.mission_lock.get()
            self.start_missions(result)
            time.sleep(0.5)
   
    @contextmanager
    def sync(self):
        """
        Internal function do synchronize jobs.
        """
        self.thread_sync_lock.acquire()
        try:  
            yield  
        except Exception, e:  
            print 'function sync got error: %s' % e  
            traceback.print_exc(file=sys.stdout)
        else:  
            self.thread_sync_lock.release()
   
    def add_missions(self, missions):
        for mission in missions:
            mission.connect("pause", self.finish_missions)
            mission.connect("resume",  self.resume_missions)
            mission.connect("stop",  self.finish_missions)
            mission.connect("finish",  self.finish_missions)
        self.mission_lock.put(missions)    
            
    def resume_missions(self, mission, data):        
        mission.connect("pause", self.finish_missions)
        mission.connect("resume",  self.resume_missions)
        mission.connect("stop",  self.finish_missions)
        mission.connect("finish",  self.finish_missions)
        
        with self.sync_lock():
            if len(self.active_mission_list) >= self.concurrent_thread_num:
                self.wait_mission_list.insert(0, mission)
            else:    
                self.start_mission(mission)
            
    def start_missions(self, missions):        
        for (index, mission) in enumerate(missions):
            # Add to wait list if active mission number reach max value.
            if len(self.active_mission_list) >= self.concurrent_thread_num:
                self.wait_mission_list += missions[index::]
                break
            
            # Otherwise start new mission.
            else:
                self.start_mission(mission)
                
    def start_mission(self, mission):            
        self.active_mission_list.append(mission)
        mission.start()
            
    def wake_up_wait_missions(self):        
        for mission in self.wait_mission_list:
            # Just break loop when active mission is bigger than max value.
            if len(self.active_mission_list) >= self.concurrent_thread_num:
                break
            # Otherwise add mission from wait list.
            else:
                # Remove from wait list.
                if mission in self.wait_mission_list:
                    self.wait_mission_list.remove(mission)
                
                # Start new mission.
                self.start_mission(mission)
        
    def finish_missions(self, mission,  data):        
        
        with self.sync():
            # Remove mission from active mission list.
            if mission in self.active_mission_list:
                mission.disconnect("pause", self.finish_missions)
                mission.disconnect("resume", self.resume_missions)
                mission.disconnect("stop", self.finish_missions)
                mission.disconnect("finish", self.finish_missions)
                self.active_mission_list.remove(mission)
                
            # Wake up wait missions.
            self.wake_up_wait_missions()
            
            # Exit thread when download finish.
            if (len(self.active_mission_list) == 0 and len(self.wait_mission_list) == 0):
                pass
                # self.mission_lock.put(self.FINISH_SIGNAL)
