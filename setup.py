#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from distutils.core import setup
import pyaspects

PYASPECTS_VERSION = pyaspects.__version__

setup(name="pyaspects",
      version= PYASPECTS_VERSION,
      description="PyAspects",
      long_description="PyAspects.",
      license="GNU GPL2",
      author="Barış Metin",
      author_email="baris@metin.org",
      url="http://www.metin.org",
      packages = ['pyaspects'],
      package_dir = {'': ''},
    )
