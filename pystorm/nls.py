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

"""
    This is the Native Language Support module.  It basically allows us to
    code in a gettext fashion without a hard depend on gettext itself.
"""

import locale

from . import xdg

try:
    # Set to user default, gracefully fallback on C otherwise
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    pass

try:
    import gettext as gettextmod

    # Required for gtk.Builder messages
    try:
        locale.textdomain('pystorm')
    except AttributeError: # E.g. Windows
        pass
    
    # Required for dynamically added messages
    gettextmod.textdomain('pystorm')

    if xdg.local_hack: # running from source dir, so we have to set the paths
        import os.path
        locale_path = os.path.join(xdg.program_dir, 'po')
        try:
            locale.bindtextdomain('pystorm', locale_path)
        except AttributeError: # E.g. Windows
            pass
        gettextmod.bindtextdomain('pystorm', locale_path)

    gettextfunc = gettextmod.gettext

    def gettext(text):
        return gettextfunc(text).decode("utf-8")

    ngettextfunc = gettextmod.ngettext

    def ngettext(singular, plural, n):
        return ngettextfunc(singular, plural, n).decode('utf-8')

except ImportError:
    # gettext is not available.  Provide a dummy function instead
    def gettext(text):
        return text

    def ngettext(singular, plural, n):
        if n == 1:
            return singular
        else:
            return plural

