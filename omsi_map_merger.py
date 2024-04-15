# Copyright 2020, 2021, 2023, 2024 Bartosz Gajewski
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

import argparse
import omsi_map
import omsi_files
import global_config
import tile
import os

class MapRepetitionError(Exception):
    pass

class LoadingMapNotInListToMergeError(Exception):
    pass

class MapToMerge:
    def __init__(self,
                 directory: str,
                 shift_x: int,
                 shift_y: int,
                 ) -> None:
        if not os.path.isdir(directory):
            raise ValueError(f"\"{directory}\" is not directory")
        self.omsi_map: omsi_map.OmsiMap = omsi_map.OmsiMap(directory)
        self.shift_x: int = shift_x
        self.shift_y: int = shift_y
    
    def __str__(self) -> str:
        return self.omsi_map.directory

class OmsiMapMerger:
    def __init__(self) -> None:
        self.__maps: list[MapToMerge] = []
        for test_map in [
            "/home/bartek/OMSI 2/maps/Podmiejska/",
            "/home/bartek/OMSI 2/maps/MZK Kydczice/",#;)
            "/home/bartek/Downloads/omsi/Städtedreieck21/OMSI 2/maps/Städtedreieck21/",
        ]:
            self.append_map(test_map)
    
    def get_maps(self) -> list[MapToMerge]:
        return self.__maps
    
    def append_map(self, directory: str) -> None:
        if os.path.normpath(directory) in map(lambda x: x.omsi_map.directory, self.__maps):
            raise MapRepetitionError(f"This map (\"{directory}\") has been added to merge before.\nMerging map with iself is not allowed.")
        self.__maps.append(MapToMerge(os.path.normpath(directory), 0, 0))# tu ma byc normpath czy w OmsiMap??
    
    def remove_map(self, index: int) -> None:
        del self.__maps[index]# tu handle exception??
    
    def load_maps(self)-> None:
        for map_to_load in self.__maps:
            map_to_load.omsi_map.load()

def merge(map1_directory,
          map2_directory,
          map2_shift_x,
          map2_shift_y,
          new_map_directory,
          keep_map2_groundtex=False):
    map1_directory = str(map1_directory)
    map2_directory = str(map2_directory)
    map2_shift_x = str(map2_shift_x)
    map2_shift_y = str(map2_shift_y)
    new_map_directory = str(new_map_directory)
    
    def aigroups_are_same_names():
        for map1_aigroup in map1._ailists.aigroups:
            for map2_aigroup in map2._ailists.aigroups:
                if map1_aigroup.name == map2_aigroup.name:
                    return True
        return False
    
    def change_map2_aigroups_names():
        while aigroups_are_same_names():
            for map2_time_table_line in map2._standard_timetable.time_table_lines:
                for tour in map2_time_table_line.tours:
                    tour.ai_group_name = "_" + tour.ai_group_name
            for aigroup in map2._ailists.aigroups:
                aigroup.name = "_" + aigroup.name
            for map2_chrono in map2._chronos:
                for time_table_line in map2_chrono.timetable.time_table_lines:
                    for tour in time_table_line.tours:
                        tour.ai_group_name = "_" + tour.ai_group_name
            
    print("Starting map merge.")
    print("map1_directory = " + map1_directory)
    print("map2_directory = " + map2_directory)
    print("map2_shift_x = " + map2_shift_x)
    print("map2_shift_y = " + map2_shift_y)
    print("keep_map2_groundtex = " + str(keep_map2_groundtex))
    
    map1 = omsi_map.OmsiMap(map1_directory)
    map2 = omsi_map.OmsiMap(map2_directory)
    
    map1.load()
    map2.load()
    
    if map1._global_config.name is not None and map2._global_config.name is not None:
        map1._global_config.name = map1._global_config.name + " & " + map2._global_config.name
    elif map1._global_config.name is not None:
        map1._global_config.name = map2._global_config.name
    
    if map1._global_config.friendlyname is not None and map2._global_config.friendlyname is not None:
        map1._global_config.friendlyname = map1._global_config.friendlyname + " & " + map2._global_config.friendlyname
    elif map1._global_config.friendlyname is not None:
        map1._global_config.friendlyname = map2._global_config.friendlyname
    
    map1_groundtex_count = len(map1._global_config.groundtex)
    
    map2.change_ids_and_tile_indexes(map1._global_config.NextIDCode, len(map1._global_config._map))
    map1._global_config.NextIDCode = map1._global_config.NextIDCode - 1 + map2._global_config.NextIDCode - 1 + 1
    
    map1._global_config.entrypoints += map2._global_config.entrypoints
    
    for tile_index in range(len(map2._global_config._map)):
        pos_x_new = str(int(map2._global_config._map[tile_index].pos_x)+int(map2_shift_x))
        pos_y_new = str(int(map2._global_config._map[tile_index].pos_y)+int(map2_shift_y))
        map1._global_config._map.append(global_config.Map(pos_x=pos_x_new,
                                                          pos_y=pos_y_new,
                                                          map_file="tile_"+pos_x_new+"_"+pos_y_new+".map"))
        
        for file in map2._tiles[tile_index]._files.omsi_files:
            file.params["pos_x"] = pos_x_new
            file.params["pos_y"] = pos_y_new
        if (keep_map2_groundtex
            and (map1._global_config.groundtex[0].tex1 != map2._global_config.groundtex[0].tex1
                 or map1._global_config.groundtex[0].tex2 != map2._global_config.groundtex[0].tex2
                 or map1._global_config.groundtex[0].num1 != map2._global_config.groundtex[0].num1
                 or map1._global_config.groundtex[0].num2 != map2._global_config.groundtex[0].num2
                 or map1._global_config.groundtex[0].num3 != map2._global_config.groundtex[0].num3
                 )
            ):
                full_covered_groundtex_file = omsi_files.OmsiFile(map_path=os.path.dirname(os.path.abspath(__file__)),
                                                                  pattern="texture/map/tile_{pos_x}_{pos_y}.map.{groundtex_index}.dds",
                                                                  params={"pos_x": 0, "pos_y": 0, "groundtex_index":0})
                full_covered_groundtex_file.params["pos_x"] = pos_x_new
                full_covered_groundtex_file.params["pos_y"] = pos_y_new
                map2._tiles[tile_index]._files.add(full_covered_groundtex_file)
        map1._tiles[len(map1._tiles)] = map2._tiles[tile_index]
    
    if map1._standard_timetable.busstops.busstops is not None and map2._standard_timetable.busstops.busstops is not None:
        map1._standard_timetable.busstops.busstops += map2._standard_timetable.busstops.busstops
    elif map2._standard_timetable.busstops.busstops is not None:
        map1._standard_timetable.busstops.busstops = map2._standard_timetable.busstops.busstops
    if map1._standard_timetable.station_links.station_link is not None and map2._standard_timetable.station_links.station_link is not None:
        map1._standard_timetable.station_links.station_link += map2._standard_timetable.station_links.station_link
    elif map2._standard_timetable.station_links.station_link is not None:
        map1._standard_timetable.station_links.station_link = map2._standard_timetable.station_links.station_link
    map1._standard_timetable.time_table_line_files += map2._standard_timetable.time_table_line_files
    map1._standard_timetable.time_table_lines += map2._standard_timetable.time_table_lines
    map1._standard_timetable.track_files += map2._standard_timetable.track_files
    map1._standard_timetable.tracks += map2._standard_timetable.tracks
    map1._standard_timetable.trip_files += map2._standard_timetable.trip_files
    map1._standard_timetable.trips += map2._standard_timetable.trips
    
    change_map2_aigroups_names()
    map1._ailists.aigroups += map2._ailists.aigroups
    
    if (keep_map2_groundtex
        and (map1._global_config.groundtex[0].tex1 != map2._global_config.groundtex[0].tex1
             or map1._global_config.groundtex[0].tex2 != map2._global_config.groundtex[0].tex2
             or map1._global_config.groundtex[0].num1 != map2._global_config.groundtex[0].num1
             or map1._global_config.groundtex[0].num2 != map2._global_config.groundtex[0].num2
             or map1._global_config.groundtex[0].num3 != map2._global_config.groundtex[0].num3
             )
        ):
        map2._global_config.groundtex[0].num1 = "3"
        for groundtex in map2._global_config.groundtex:
            map1._global_config.groundtex.append(groundtex)
        map2.change_groundtex_indexes(map1_groundtex_count)
    else:
        for groundtex in map2._global_config.groundtex[1:]:
            map1._global_config.groundtex.append(groundtex)
        map2.change_groundtex_indexes(map1_groundtex_count-1)
    
    for chrono in map2._chronos:
        for chrono_tile_info in chrono.chrono_tiles_infos:
            chrono_tile_info.pos_x = str(int(chrono_tile_info.pos_x)+int(map2_shift_x))
            chrono_tile_info.pos_y = str(int(chrono_tile_info.pos_y)+int(map2_shift_y))
    map1._chronos += map2._chronos
    
    map1.directory = new_map_directory
    map1.save()
    print("Done.")

if __name__ == "__main__":
    arguments_parser = argparse.ArgumentParser(description="OMSI Map Merger")
    arguments_parser.add_argument("map1_directory", help="Directory of 1st map", type=str)
    arguments_parser.add_argument("map2_directory", help="Directory of 2nd map", type=str)
    arguments_parser.add_argument("map2_shift_x", help="Horizontal shift of 2nd map (tiles)", type=int)
    arguments_parser.add_argument("map2_shift_y", help="Vertical shift of 2nd map (tiles)", type=int)
    arguments_parser.add_argument("new_map_directory", help="Directory of new map", type=str)
    parsed_arguments = arguments_parser.parse_args()
    merge(parsed_arguments.map1_directory,
          parsed_arguments.map2_directory,
          parsed_arguments.map2_shift_x,
          parsed_arguments.map2_shift_y,
          parsed_arguments.new_map_directory)
