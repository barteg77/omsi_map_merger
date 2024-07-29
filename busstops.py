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

class Busstop:
    def __init__(self,
                 name: str,
                 tile_index: int,
                 id: int,
                 exiting_passengers: int,
                 line4: str,
                 line5: str,
                 subname: str,
                 ):
        self.name: str = name
        self.tile_index: int = tile_index
        self.id: int = id
        self.exiting_passengers: int = exiting_passengers
        self.line4: str = line4
        self.line5: str = line5
        self.subname: str = subname

class Busstops:
    def __init__(self,
                 comment1: str,
                 comment2: str,
                 busstops: list[Busstop]):
        self.comment1: str = comment1
        self.comment2: str = comment2
        self.busstops: list[Busstop] = busstops
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int):
        if self.busstops is not None:
            for busstop in self.busstops:
                busstop.tile_index = busstop.tile_index + tile_indices_value
                busstop.id = busstop.id + ids_value
