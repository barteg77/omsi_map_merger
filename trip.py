# Copyright 2020, 2024 Bartosz Gajewski
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

import typing

class AnyStation:
    def __init__(self):
        self.id: int
        raise NotImplementedError

class Station(AnyStation):
    def __init__(self,
                 id: int,
                 interval,
                 name,
                 tile_index: int,
                 line5,
                 line6,
                 line7,
                 line8,
                 ):
        self.id: int = id
        self.interval = interval
        self.name = name
        self.tile_index: int = tile_index
        self.line5 = line5
        self.line6 = line6
        self.line7 = line7
        self.line8 = line8

class StationTyp2(AnyStation):
    def __init__(self, id: int):
        self.id: int = id

class Trip:
    def __init__(self,
                 comment1,
                 comment2,
                 line1,
                 line2,
                 line3,
                 station: list[Station] | list[StationTyp2],
                 lines=None,
                 ):
        self.comment1 = comment1
        self.comment2 = comment2
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.station: list[Station] | list[StationTyp2] = station
        self.lines = lines
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int):
        for station in self.station:
            station.id += ids_value
            if type(station) == Station:
                typing.cast(Station, station).tile_index += tile_indices_value