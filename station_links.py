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

class StationLinkEntry:
    def __init__(self,
                 comment=None,
                 id=None,
                 line2=None,
                 tile_index=None,
                 length=None,
                 line5=None,
                 line6=None,
                 line7=None,
                 chrono_files=None
                 ):
        self.comment = comment
        self.id = id
        self.line2 = line2
        self.tile_index = tile_index
        self.length = length
        self.line5 = line5
        self.line6 = line6
        self.line7 = line7
        self.chrono_files = chrono_files

class StationLink:
    def __init__(self,
                 comment=None,
                 line1=None,
                 id_busstop_start=None,
                 id_busstop_end=None,
                 line4=None,
                 line5=None,
                 line6=None,
                 line7=None,
                 line8=None,
                 line9=None,
                 station_link_entry=None
                 ):
        self.comment = comment
        self.line1 = line1
        self.id_busstop_start = id_busstop_start
        self.id_busstop_end = id_busstop_end
        self.line4 = line4
        self.line5 = line5
        self.line6 = line6
        self.line7 = line7
        self.line8 = line8
        self.line9 = line9
        self.station_link_entry = station_link_entry

class StationLinks:
    def __init__(self,
                 comment1=None,
                 comment2=None,
                 station_link=None):
        self.comment1 = comment1
        self.comment2 = comment2
        self.station_link = station_link
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        if self.station_link is not None:
            for station_link in self.station_link:
                station_link.id_busstop_start = str(int(station_link.id_busstop_start) + int(ids_value))
                station_link.id_busstop_end = str(int(station_link.id_busstop_end) + int(ids_value))
                for station_link_entry in station_link.station_link_entry:
                    station_link_entry.id = str(int(station_link_entry.id) + int(ids_value))
                    station_link_entry.tile_index = str(int(station_link_entry.tile_index) + int(tile_indexes_value))
