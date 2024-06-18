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

import omsi_map
import global_config
import os
import itertools
import operator
import version

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
                 keep_groundtex: bool,
                 ) -> None:
        if not os.path.isdir(directory):
            raise ValueError(f"\"{directory}\" is not directory")
        super().__init__(directory)
        self.shift_x: int = shift_x
        self.shift_y: int = shift_y
        self.__keep_groundtex: bool = keep_groundtex
    
    def __str__(self) -> str:
        return self.directory
    
    def get_shift_x(self) -> int:
        return self.shift_x
    
    def get_shift_y(self) -> int:
        return self.shift_y
    
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

def shifted_entrypoint(entrypoint: global_config.Entrypoints, shift_idcode: int, shift_tile_index: int,) -> global_config.Entrypoints:
    return global_config.Entrypoints(entrypoint.object_on_tile_index,
                                        entrypoint.id + shift_idcode,
                                        entrypoint.line3,
                                        entrypoint.line4,
                                        entrypoint.line5,
                                        entrypoint.line6,
                                        entrypoint.line7,
                                        entrypoint.line8,
                                        entrypoint.line9,
                                        entrypoint.line10,
                                        entrypoint.tile_index + shift_tile_index,
                                        entrypoint.name)

def shifted_entrypoints(entrypoints: list[global_config.Entrypoints], shift_idcode: int, shift_tile_index: int) -> list[global_config.Entrypoints]:
    return [shifted_entrypoint(entrypoint, shift_idcode, shift_tile_index) for entrypoint in entrypoints]

def shifted_gc_tile(gc_tile: global_config.Map, shift_x: int, shift_y: int) -> global_config.Map:
    pos_x: int = gc_tile.pos_x + shift_x
    pos_y: int = gc_tile.pos_y + shift_y
    return global_config.Map(pos_x,
                             pos_y,
                             f'tile_{pos_x}_{pos_y}.map')

def shifted_gc_tiles(gc_tiles: list[global_config.Map], shift_x: int, shift_y: int) -> list[global_config.Map]:
    return [shifted_gc_tile(gc_tile, shift_x, shift_y) for gc_tile in gc_tiles]

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
        return all([mtm.ready() for mtm in self.get_maps()]) and not self.overlapping() and len(self.get_maps()) >= 2
    
    def merged_gc_groundtex(self) -> list[global_config.GroundTex]:
        assert not self.get_maps()[0].get_keep_groundtex() # to do: blokada w gui
        groundtex: list[global_config.GroundTex] = [self.get_maps()[0].get_global_config().get_data().groundtex[0]]
        for mtm in self.get_maps():
            all_groundtex: list[global_config.GroundTex] = mtm.get_global_config().get_data().groundtex
            groundtex_to_copy: list[global_config.GroundTex] = all_groundtex if mtm.get_keep_groundtex() else all_groundtex[1:]
            groundtex += groundtex_to_copy
        return groundtex
    
    def merged_groundtex_shift(self) -> dict[MapToMerge, int]:
        groundtex_shifts_sequentially: list[int] = [0]
        for mtm in self.get_maps():
            all_groundtex_ct: int = len(mtm.get_global_config().get_data().groundtex)
            kept_groundtex_ct: int = all_groundtex_ct if mtm.get_keep_groundtex() else all_groundtex_ct-1
            groundtex_shifts_sequentially.append(groundtex_shifts_sequentially[-1] + kept_groundtex_ct)
        return dict(zip(self.get_maps(), groundtex_shifts_sequentially))
    
    def merged_idcodes_shifts(self) -> dict[MapToMerge, int]:
        next_idcodes_sequentially: list[int] = [mtm.get_global_config().get_data().NextIDCode for mtm in self.get_maps()]
        return dict(zip(self.get_maps(), itertools.accumulate([0] + next_idcodes_sequentially, operator.add)))
    
    def merged_tiles_indices_shift(self) -> dict[MapToMerge, int]:
        tiles_counts_sequentially: list[int] = [len(mtm.get_global_config().get_data()._map) for mtm in self.get_maps()]
        return dict(zip(self.get_maps(), itertools.accumulate([0] + tiles_counts_sequentially, operator.add)))

    def merged_omsi_map(self, new_map_name: str) -> omsi_map.OmsiMap:
        assert self.ready(), "You can't get merged omsi map while not all maps are ready"
        assert not self.get_maps()[0].get_keep_groundtex(), "\"Keep groundtex\" on 1st map is nonsense."
        
        comment: str = "File created with OMSI Map Merger {version.version}"
        new_om: omsi_map.OmsiMap = omsi_map.OmsiMap("to be set later")

        idcode_shift: dict[MapToMerge, int] = self.merged_idcodes_shifts()
        tile_shift: dict[MapToMerge, int] = self.merged_tiles_indices_shift()

        # constructing global config
        map_description: str = f"{new_map_name}\nMap created with OMSI Map Merger {version.version}\nMerged maps (path, shift_x, shift_y, keep_groundtex):\n"\
        + "".join(["\n* " + ", ".join([mtm.get_directory(), str(mtm.get_shift_x()), str(mtm.get_shift_y()), str(mtm.get_keep_groundtex())]) for mtm in self.get_maps()])
        
        gc_entrypoints: list[global_config.Entrypoints] = list(itertools.chain.from_iterable([shifted_entrypoints(mtm._global_config.get_data().entrypoints,
                                                                                                               idcode_shift[mtm],
                                                                                                               tile_shift[mtm]) for mtm in self.get_maps()]))
        gc_tiles: list[global_config.Map] = list(itertools.chain.from_iterable([shifted_gc_tiles(mtm._global_config.get_data()._map,
                                                                                                 mtm.get_shift_x(),
                                                                                                 mtm.get_shift_y()) for mtm in self.get_maps()]))
        gc: global_config.GlobalConfig
        gc = global_config.GlobalConfig(comment,
                                        new_map_name,
                                        new_map_name,
                                        map_description,
                                        '14',
                                        sum([mtm.get_global_config().get_data().NextIDCode for mtm in self.get_maps()]),
                                        False,
                                        False,
                                        False,
                                        self.get_maps()[0].get_global_config().get_data().backgroundimage,
                                        self.get_maps()[0].get_global_config().get_data().mapcam,
                                        self.get_maps()[0].get_global_config().get_data().moneysystem,
                                        self.get_maps()[0].get_global_config().get_data().ticketpack,
                                        self.get_maps()[0].get_global_config().get_data().repair_time_min,
                                        self.get_maps()[0].get_global_config().get_data().years,
                                        self.get_maps()[0].get_global_config().get_data().realyearoffset,
                                        self.get_maps()[0].get_global_config().get_data().standarddepot,
                                        self.merged_gc_groundtex(),
                                        self.get_maps()[0].get_global_config().get_data().addseason,
                                        self.get_maps()[0].get_global_config().get_data().trafficdensity_road,
                                        self.get_maps()[0].get_global_config().get_data().trafficdensity_passenger,
                                        gc_entrypoints,
                                        gc_tiles,
                                        )
        new_om.get_global_config().set_external_data(gc)
            
        print('merged')
        return new_om