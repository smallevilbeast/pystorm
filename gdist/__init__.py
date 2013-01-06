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

"""distutils extensions for GTK+/GObject/Unix

This module contains a Distribution subclass (GDistribution) which
implements build and install commands for operations related to
Python GTK+ and GObject support. This includes installation
of man pages and gettext/intltool support.
"""

import os

try:
    from py2exe import Distribution
except ImportError:
    from distutils.core import Distribution

from distutils.command.build import build as distutils_build
from distutils.command.install import install as distutils_install

from gdist.po import build_mo, install_mo, po_stats, check_pot


class build(distutils_build):
    """Override the default build with new subcommands."""
    sub_commands = distutils_build.sub_commands + [
        ("build_mo",
         lambda self: self.distribution.has_po())]

class install(distutils_install):
    """Override the default install with new subcommands."""

    sub_commands = distutils_install.sub_commands + [
        ("install_mo", lambda self: self.distribution.has_po())]

class GDistribution(Distribution):
    """A Distribution with support for GTK+-related options

    The GDistribution class adds a number of commads and parameters
    related to GTK+ and GObject Python programs and libraries.

    Parameters (to distutils.core.setup):
      po_directory -- directory where .po files are contained
      po_package -- package name for translation files
      shortcuts -- list of .desktop files to build/install
      man_pages -- list of man pages to install

    Using the translation features requires intltool.

    Example:
      from distutils.core import setup
      from gdist import GDistribution

      setup(distclass=GDistribution, ...)
      """

    shortcuts = []
    po_directory = None
    man_pages = []
    po_package = None

    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)
        self.cmdclass.setdefault("build_mo", build_mo)
        self.cmdclass.setdefault("install_mo", install_mo)
        self.cmdclass.setdefault("build", build)
        self.cmdclass.setdefault("install", install)
        self.cmdclass.setdefault("po_stats", po_stats)
        self.cmdclass.setdefault("check_pot", check_pot)

    def has_po(self):
        return os.name != 'nt' and bool(self.po_directory)

    def has_shortcuts(self):
        return os.name != 'nt' and bool(self.shortcuts)

    def has_man_pages(self):
        return os.name != 'nt' and bool(self.man_pages)

    def need_icon_cache(self):
        return os.name != 'nt'

    def need_icon_install(self):
        return os.name != 'nt'

__all__ = ["GDistribution"]
