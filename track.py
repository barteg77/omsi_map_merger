# Copyright 2020, 2024, 2025 Bartosz Gajewski
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

class TrackEntry:
    def __init__(self,
                 comment: str,
                 id: int,
                 line2: str,
                 tile_index: int,
                 line4: str,
                 length: str,
                 line6: str,
                 line7: str
                 ):
        self.comment: str = comment
        self.id: int = id
        self.line2: str = line2
        self.tile_index: int = tile_index
        self.line4: str = line4
        self.length: str = length
        self.line6: str = line6
        self.line7: str = line7

class Track:
    def __init__(self,
                 comment1: str,
                 comment2: str,
                 track_entry: list[TrackEntry]):
        self.comment1: str = comment1
        self.comment2: str = comment2
        self.track_entry: list[TrackEntry] = track_entry
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int):
        for te in self.track_entry:
            te.id = te.id + ids_value
            te.tile_index = te.tile_index + tile_indices_value
