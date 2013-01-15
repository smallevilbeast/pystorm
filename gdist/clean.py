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

"""clean up output of 'build' commands"""

import os

from distutils.core import Command
from distutils.command.clean import clean as distutils_clean

class clean(distutils_clean, Command):
    """clean up output of 'build' commands

    GDistribution commands generate files that the normal distutils
    clean command doesn't. This removes them.
    """

    description = "clean up output of 'build' commands"

    def initialize_options(self):
        distutils_clean.initialize_options(self)

    def finalize_options(self):
        distutils_clean.finalize_options(self)
        self.po_package = self.distribution.po_package
        self.po_directory = self.distribution.po_directory

    def run(self):
        distutils_clean.run(self)
        if self.all:
            if self.po_directory and self.po_package:
                pot = os.path.join(self.po_directory, self.po_package + ".pot")
                try: os.unlink(pot)
                except OSError: pass

__all__ = ["clean"]
