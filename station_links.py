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

class StationLinkEntry:
    def __init__(self,
                 comment: str,
                 id: int,
                 line2: str,
                 tile_index: int,
                 length: str,
                 line5: str,
                 line6: str,
                 line7: str,
                 chrono_files=None
                 ):
        self.comment: str = comment
        self.id: int = id
        self.line2: str = line2
        self.tile_index: int = tile_index
        self.length: str = length
        self.line5: str = line5
        self.line6: str = line6
        self.line7: str = line7
        self.chrono_files = chrono_files#???????????

class StationLink:
    def __init__(self,
                 comment: str,
                 line1: str,
                 id_busstop_start: int,
                 id_busstop_end: int,
                 line4: str,
                 line5: str,
                 line6: str,
                 line7: str,
                 line8: str,
                 line9: str,
                 station_link_entry: list[StationLinkEntry],
                 ):
        self.comment: str = comment
        self.line1: str = line1
        self.id_busstop_start: int = id_busstop_start
        self.id_busstop_end: int = id_busstop_end
        self.line4: str = line4
        self.line5: str = line5
        self.line6: str = line6
        self.line7: str = line7
        self.line8: str = line8
        self.line9: str = line9
        self.station_link_entry: list[StationLinkEntry] = station_link_entry

class StationLinks:
    def __init__(self,
                 comment1: str,
                 comment2: str,
                 station_link: list[StationLink]):
        self.comment1: str = comment1
        self.comment2: str = comment2
        self.station_link: list[StationLink] = station_link
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int) -> None:
        for station_link in self.station_link:
            station_link.id_busstop_start = station_link.id_busstop_start + ids_value
            station_link.id_busstop_end = station_link.id_busstop_end + ids_value
            for station_link_entry in station_link.station_link_entry:
                station_link_entry.id = station_link_entry.id + ids_value
                station_link_entry.tile_index = station_link_entry.tile_index + tile_indices_value
