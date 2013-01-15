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
import math

from .nls import gettext as _

def parse_bytes(bytes):
    if bytes == 0:
        return "0b"
    k = math.log(bytes, 1024)
    ret_str = "%.2f%s" % (bytes / (1024.0 ** int(k)), "bKMGTPEY"[int(k)])
    return ret_str

def parse_time(time_in_secs):
    ret_str = ""
    mult_list = [60, 60 * 60, 60 * 60 * 24]
    unit_list = [_("second(s)"), _("minute(s)"), _("hour(s)"), _("day(s)")]
    for i in range(len(mult_list)):
        if time_in_secs < mult_list[i]:
            pval = int(time_in_secs / (mult_list[i - 1] if i > 0 else 1))
            ret_str = "%d %s" % (pval, unit_list[i])
            break
    if len(ret_str) == 0:
        ret_str = "%d %s" % (int(time_in_secs / mult_list[2]), \
                                  unit_list[3])
    return ret_str

class ProgressBar(object):
    
    def __init__(self, n_conn, conn_state):
        self.n_conn = n_conn
        self.dots = ["" for i in range(n_conn)]
        self.conn_state = conn_state

    def _get_term_width(self):
        platform = sys.platform
        default_cols = 75
        if platform.startswith("linux"):
            try:
                term_rows, term_cols = map(int, os.popen('stty size', 'r').read().split())
            except:    
                return default_cols
            else:
                return term_cols
        else:    
            return default_cols

    def _get_download_rate(self, bytes):
        ret_str = parse_bytes(bytes)
        ret_str += "/s."
        return len(ret_str), ret_str

    def _get_percentage_complete(self, dl_len):
        assert self.conn_state.filesize != 0
        ret_str = str(dl_len * 100 / self.conn_state.filesize) + "%."
        return len(ret_str), ret_str

    def _get_time_left(self, time_in_secs):
        ret_str = ""
        mult_list = [60, 60 * 60, 60 * 60 * 24]
        unit_list = [_("second(s)"), _("minute(s)"), _("hour(s)"), _("day(s)")]
        for i in range(len(mult_list)):
            if time_in_secs < mult_list[i]:
                pval = int(time_in_secs / (mult_list[i - 1] if i > 0 else 1))
                ret_str = "%d %s" % (pval, unit_list[i])
                break
        if len(ret_str) == 0:
            ret_str = "%d %s." % (int(time_in_secs / mult_list[2]), \
                                      unit_list[3])
        return len(ret_str), ret_str

    def _get_pbar(self, width):
        ret_str = "["
        for i in range(self.n_conn):
            dots_list = ['=' for j in range((self.conn_state.progress[i] *
                                             width) /
                                            self.conn_state.chunks[i])]
            self.dots[i] = "".join(dots_list)
            if ret_str == "[":
                ret_str += self.dots[i]
            else:
                ret_str += "|" + self.dots[i]
            if len(self.dots[i]) < width:
                ret_str += '>'
                ret_str += "".join([' ' for i in range(width -
                                                       len(self.dots[i]) - 1)])

        ret_str += "]"
        return len(ret_str), ret_str

    def display_progress(self):
        dl_len = 0
        for rec in self.conn_state.progress:
            dl_len += rec

        try:
            avg_speed = dl_len / self.conn_state.elapsed_time
        except:    
            avg_speed = 0

        ldr, drate = self._get_download_rate(avg_speed)
        lpc, pcomp = self._get_percentage_complete(dl_len)
        ltl, tleft = self._get_time_left((self.conn_state.filesize - dl_len) /
                                         avg_speed if avg_speed > 0 else 0)
        # term_width - #(|) + #([) + #(]) + #(strings) +
        # 6 (for spaces and periods)
        available_width = self._get_term_width() - (ldr + lpc +
                                                        ltl) - self.n_conn - 1 - 6
        lpb, pbar = self._get_pbar(available_width / self.n_conn)
        sys.stdout.flush()
        print "\r%s %s %s %s" % (drate, pcomp, tleft, pbar),
            
