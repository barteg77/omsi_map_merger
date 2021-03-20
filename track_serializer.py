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

class TrackSerializer:
    def serialize(self, track_class, file_name):
        with open(file_name, 'w', encoding='iso-8859-1', newline='\r\n') as f:
            self.serialize_(track_class, f)
    
    def serialize_(self, track_class, f):
        print("-----------------------", file=f)
        print("Time Table Track File", file=f)
        print("-----------------------", file=f)
        print(file=f)
        print(track_class.comment1, file=f)
        print(track_class.comment2, file=f)
        print(file=f)
        if track_class.track_entry is not None:
            for te in track_class.track_entry:
                print(te.comment, file=f)
                print("[track_entry]", file=f)
                print(te.id, file=f)
                print(te.line2, file=f)
                print(te.tile_index, file=f)
                print(te.line4, file=f)
                print(te.length, file=f)
                print(te.line6, file=f)
                if te.line7 is not None:
                    print(te.line7, file=f)
                print(file=f)
