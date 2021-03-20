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

import station_links

class StationLinksSerializer:
    def serialize(self, station_links_class, file_name):
        with open(file_name, 'w', encoding='iso-8859-1', newline='\r\n') as f:
            self.serialize_(station_links_class, f)
    
    def serialize_(self, station_links_class, f):
        print("---------------------------", file=f)
        print("Time Table StnLinkList File", file=f)
        print("---------------------------", file=f)
        print(file=f)
        print(station_links_class.comment1, file=f)
        print(station_links_class.comment2, file=f)
        print(file=f)
        if station_links_class.station_link is not None:
            for station_link in station_links_class.station_link:
                print(station_link.comment, file=f)
                print(file=f)
                print("[StnLink]", file=f)
                print(station_link.line1, file=f)
                print(station_link.id_busstop_start, file=f)
                print(station_link.id_busstop_end, file=f)
                print(station_link.line4, file=f)
                print(station_link.line5, file=f)
                print(station_link.line6, file=f)
                print(station_link.line7, file=f)
                print(station_link.line8, file=f)
                print(station_link.line9, file=f)
                print(file=f)
                if station_link.station_link_entry is not None:
                    for station_link_entry in station_link.station_link_entry:
                        print(station_link_entry.comment, file=f)
                        print("[StnLink_entry]", file=f)
                        print(station_link_entry.id, file=f)
                        print(station_link_entry.line2, file=f)
                        print(station_link_entry.tile_index, file=f)
                        print(station_link_entry.length, file=f)
                        print(station_link_entry.line5, file=f)
                        print(station_link_entry.line6, file=f)
                        print(station_link_entry.line7, file=f)
                        if station_link_entry.chrono_files is not None:
                            for chrono_file in station_link_entry.chrono_files:
                                print(chrono_file, file=f)
                        print(file=f)
