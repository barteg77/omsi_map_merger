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

import busstops

class BusstopsSerializer:
    def serialize(self, busstops: busstops.Busstops, file_name):
        with open(file_name, 'w', encoding='iso-8859-1', newline='\r\n') as f:
            self.serialize_(busstops, f)
    
    def serialize_(self, busstops: busstops.Busstops, f):
        print("---------------------------", file=f)
        print("Time Table BusStopList File", file=f)
        print("---------------------------", file=f)
        print(file=f)
        print(busstops.comment1, file=f)
        print(busstops.comment2, file=f)
        print(file=f)
        for busstop in busstops.busstops:
            print("[busstop]", file=f)
            print(busstop.name, file=f)
            print(busstop.tile_index, file=f)
            print(busstop.id, file=f)
            print(busstop.exiting_passengers, file=f)
            print(busstop.line4, file=f)
            print(busstop.line5, file=f)
            print(busstop.subname, file=f)
            print(file=f)
