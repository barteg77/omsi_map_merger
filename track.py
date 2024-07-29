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

class TrackEntry:
    def __init__(self,
                 comment=None,
                 id=None,
                 line2=None,
                 tile_index=None,
                 line4=None,
                 length=None,
                 line6=None,
                 line7=None
                 ):
        self.comment = comment
        self.id = id
        self.line2 = line2
        self.tile_index = tile_index
        self.line4 = line4
        self.length = length
        self.line6 = line6
        self.line7 = line7

class Track:
    def __init__(self,
                 comment1=None,
                 comment2=None,
                 track_entry=[]):
        self.comment1 = comment1
        self.comment2 = comment2
        self.track_entry = track_entry
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int):
        if self.track_entry is not None:
            for te in self.track_entry:
                te.id = str(int(te.id) + ids_value)
                te.tile_index = str(int(te.tile_index) + tile_indices_value)
