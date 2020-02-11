# coding: utf-8
# pylint: disable=F0401,C0111,W0232,E1101,E1103,C0301,C0103,W0614,W0401,E0202

# Copyright 2020 by Leipzig University Library, http://ub.uni-leipzig.de
#                   The Finc Authors, http://finc.info
#                   Martin Czygan, <martin.czygan@uni-leipzig.de>
#
# This file is part of some open source application.
#
# Some open source application is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Some open source application is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Helper functions for generating filter config files.

A filterconfig is a JSON file that expresses what an instituition or project
wants (or is allowed) to access from a shared index (expressed as YAML at
[https://git.io/JvC0T](https://git.io/JvC0T)). More examples at
[https://git.io/JvC0L](https://git.io/JvC0L).

"""

import collections

Entry = collections.namedtuple('Entry', 'sid collection kbart package')

class FilterConfig:
    """
    Config accumulator and serializer.
    """
    def __init__(self):
        self.map = collections.defaultdict(list)

    def add(self, isil=None, sid=None, collection=None, kbart=None, package=None):
        """
        Say: isil wants to see sid and maybe one or more collections and
        holding files.
        """
        # TODO(martin): listify more.
        if isinstance(collection, str):
            entry = Entry(sid=sid, collection=collection, kbart=kbart, package=package)
            self.map[isil].append(entry)
        elif isinstance(collection, (tuple, list, set)):
            for c in collection:
                entry = Entry(sid=sid, collection=collection, kbart=kbart, package=package)
                self.map[isil].append(entry)
        else:
            raise ValueError('collection must be a string or list like')

    def to_dict(self):
        """
        Return the dict, that will be used for JSON export.
        """

    def to_json(self):
        """
        Return filterconfig JSON.
        """
