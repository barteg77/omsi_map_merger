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

class Station:
    def __init__(self,
                 id=None,
                 interval=None,
                 name=None,
                 tile_index=None,
                 line5=None,
                 line6=None,
                 line7=None,
                 line8=None
                 ):
        self.id = id
        self.interval = interval
        self.name = name
        self.tile_index = tile_index
        self.line5 = line5
        self.line6 = line6
        self.line7 = line7
        self.line8 = line8

class Trip:
    def __init__(self,
                 comment1=None,
                 comment2=None,
                 line1=None,
                 line2=None,
                 line3=None,
                 station=None,
                 lines=None
                 ):
        self.comment1 = comment1
        self.comment2 = comment2
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.station = station
        self.lines = lines
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        if self.station is not None:
            if isinstance(self.station[0], Station):
                for station in self.station:
                    station.id = str(int(station.id) + int(ids_value))
                    station.tile_index = str(int(station.tile_index) + int(tile_indexes_value))
            else:
                self.station = [str(int(station) + int(ids_value)) for station in self.station]
