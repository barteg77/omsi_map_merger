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

class Busstop:
    def __init__(self,
                 name=None,
                 tile_index=None,
                 id=None,
                 exiting_passengers=None,
                 line4=None,
                 line5=None,
                 subname=None):
        self.name = name
        self.tile_index = tile_index
        self.id = id
        self.exiting_passengers = exiting_passengers
        self.line4 = line4
        self.line5 = line5
        self.subname = subname

class Busstops:
    def __init__(self,
                 comment1=None,
                 comment2=None,
                 busstops=None):
        self.comment1 = comment1
        self.comment2 = comment2
        self.busstops = busstops
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        if self.busstops is not None:
            for busstop in self.busstops:
                busstop.tile_index = str(int(busstop.tile_index) + int(tile_indexes_value))
                busstop.id = str(int(busstop.id) + int(ids_value))
