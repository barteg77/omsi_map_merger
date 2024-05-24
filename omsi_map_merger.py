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
import os

class MapRepetitionError(Exception):
    pass

class LoadingMapNotInListToMergeError(Exception):
    pass

class TilePos:
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
    ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def __key(self):
        return (self.pos_x, self.pos_y)
    
    def __eq__(self, other: 'TilePos') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class MapToMerge(omsi_map.OmsiMap):
    def __init__(self,
                 directory: str,
                 shift_x: int,
                 shift_y: int,
                 ) -> None:
        if not os.path.isdir(directory):
            raise ValueError(f"\"{directory}\" is not directory")
        super().__init__(directory)
        self.shift_x: int = shift_x
        self.shift_y: int = shift_y
    
    def __str__(self) -> str:
        return self.directory
    
    def get_shifted_tiles_pos(self) -> list[TilePos]:
        return [TilePos(int(tile.pos_x) + self.shift_x,
                        int(tile.pos_y) + self.shift_y) for tile in self.get_global_config().get_data()._map]
    
    def shift(self,
              shift_x: int = 0,
              shift_y: int = 0,
    ) -> None:
        self.shift_x += shift_x
        self.shift_y += shift_y
    
    def get_keep_groundtex(self) -> bool:
        return self.__keep_groundtex
    
    def toggle_keep_groundtex(self) -> None:
        self.__keep_groundtex = not self.get_keep_groundtex()

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
    
    def get_maps_shifted_tiles_pos(self) -> list[list[TilePos]]:
        return [mtm.get_shifted_tiles_pos() for mtm in self.get_maps()]
    
    def get_graph_data(self) -> dict[TilePos, list[MapToMerge]]:
        graph_data: dict[TilePos, list[MapToMerge]] = {}
        for mtm, shifted_tiles_pos in zip(self.get_maps(), self.get_maps_shifted_tiles_pos()):
            for tile_pos in shifted_tiles_pos:
                if tile_pos not in graph_data:
                    graph_data[tile_pos] = []
                graph_data[tile_pos].append(mtm)
        return graph_data
    
    def overlapping(self) -> bool:
        return any([len(maps_on_tile) > 1 for maps_on_tile in self.get_graph_data().values()])
    
    def append_map(self, directory: str) -> None:
        if os.path.normpath(directory) in map(lambda om: om.directory, self.__maps):
            raise MapRepetitionError(f"This map (\"{directory}\") has been added to merge before.\nMerging map with iself is not allowed.")
        self.__maps.append(MapToMerge(os.path.normpath(directory), 0, 0, False))# tu ma byc normpath czy w OmsiMap??
    
    def remove_map(self, index: int) -> None:
        del self.__maps[index]# tu handle exception??
    
    def load_maps(self) -> None:
        for map_to_load in self.__maps:
            map_to_load.load()
    
    def ready(self) -> bool:
        return all([mtm.ready() for mtm in self.get_maps()])
    
    def mergedOmsiMap(self):
        if not self.ready():
            raise Exception("You can't get merged omsi map while not all maps are ready")
        