# Copyright 2020 Bartosz Gajewski
#
# This file is part of OMSI Map Merger.
#
# OMSI Map Merger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# OMSI Map Merger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OMSI Map Merger. If not, see <http://www.gnu.org/licenses/>.

import tile
class Select:
    def __init__(self,
                 spline,
                 id,
                 lines=None):
        self.spline = spline
        self.id = id
        self.lines = lines

class ChronoTile:
    def __init__(self,
                 initial_comment,
                 version,
                 list=None):
        self.initial_comment = initial_comment
        self.version = version
        self.list = list

    def change_ids(self, value):
        if list is not None:
            for entry in self.list:
                entry.id = str(int(entry.id) + int(value))
                if isinstance(entry, tile.Spline):
                    entry.id_previous = str(int(entry.id_previous) + int(value))
                    entry.id_next = str(int(entry.id_next) + int(entry.value))
                if (isinstance(entry, tile._Object) or isinstance(entry, tile.SplineAttachement) or isinstance(entry, tile.SplineAttachement)) and entry.varparent is not None:
                    entry.varparent = str(int(entry.varparent) + int(value))
