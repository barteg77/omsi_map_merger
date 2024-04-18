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

import os
import glob
import pathlib
import global_config
import global_config_parser
import global_config_serializer
import tile
import tile_parser
import tile_serializer
import omsi_files
import timetable
import ailists
import ailists_parser
import ailists_serializer
import chrono
import loader

GLOBAL_CONFIG_FILENAME = "global.cfg"
AILISTS_FILENAME = "ailists.cfg"

_global_config_parser = global_config_parser.GlobalConfigParser()
_global_config_serializer = global_config_serializer.GlobalConfigSerializer()

_tile_parser = tile_parser.TileParser()
_tile_serializer = tile_serializer.TileSerializer()

_ailists_parser = ailists_parser.AIListsParser()
_ailists_serializer = ailists_serializer.AIListsSerializer()

class GlobalConfigLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path, "gc") 
        self.data: global_config.GlobalConfig = None
        #self.__path: str = path

    def load(self) -> None:
        self.data = _global_config_parser.parse(self.path)

class TileLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path, "tile") 
        self.data: tile.Tile = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: tile.Tile = _tile_parser.parse(self.path)

class AilistsLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path, "ailists") 
        self.data: ailists.AILists = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data = _ailists_parser.parse(self.path)

class OmsiMap(loader.SafeLoaderList):
    def set_tiles_and_chronos_gc_consistent(self) -> None:
        self.empty_tiles_and_chronos()
        # set tiles' safe parsers
        tiles_safe_loaders: list[SafeLoaderUnit] = []
        groundtex_count = len(self._global_config.get_data().groundtex)
        for gc_tile in self._global_config.get_data()._map:
            tile_files = omsi_files.OmsiFiles([
                omsi_files.OmsiFile(map_path=self.directory,
                                    pattern="tile_{pos_x}_{pos_y}.map.terrain",
                                    params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y},
                                    optional=True),
                omsi_files.OmsiFile(map_path=self.directory,
                                    pattern="tile_{pos_x}_{pos_y}.map.water",
                                    params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y},
                                    optional=True),
                omsi_files.OmsiFile(map_path=self.directory,
                                    pattern="tile_{pos_x}_{pos_y}.map.LM.bmp",
                                    params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y},
                                    optional=True),
                omsi_files.OmsiFile(map_path=self.directory,
                                    pattern="texture/map/tile_{pos_x}_{pos_y}.map.roadmap.bmp",
                                    params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y},
                                    optional=True),
            ] + [ omsi_files.OmsiFile(map_path=self.directory,
                                      pattern="texture/map/tile_{pos_x}_{pos_y}.map.{groundtex_index}.dds",
                                      params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y, "groundtex_index": groundtex_index},
                                      optional=True)
                  for groundtex_index in range(1, groundtex_count+1) ])
            tiles_safe_loaders.append(loader.SafeLoaderUnit(TileLoader(os.path.join(self.directory, gc_tile.map_file)), ofiles=tile_files))
        self._tiles.set_data(tiles_safe_loaders)
        self.scan_chrono()
    
    def empty_tiles_and_chronos(self) -> None:
        self._tiles.set_data([])
        self._chronos.set_data([])

    def __init__(self,
                 directory=""):
        self.directory = directory
        self._global_config: loader.SafeLoaderUnit = loader.SafeLoaderUnit(GlobalConfigLoader(os.path.join(self.directory, GLOBAL_CONFIG_FILENAME)),
                                                                           self.set_tiles_and_chronos_gc_consistent, # on success
                                                                           self.empty_tiles_and_chronos, # on fail
                                                                           )
        self._tiles: loader.SafeLoaderList = loader.SafeLoaderList([], "Tiles")
        self._files: omsi_files.OmsiFiles = omsi_files.OmsiFiles()
        self._standard_timetable: timetable.Timetable = timetable.Timetable(self.directory)
        self._ailists: loader.SafeLoaderUnit = loader.SafeLoaderUnit(AilistsLoader(os.path.join(self.directory, AILISTS_FILENAME)))
        self._chronos: loader.SafeLoaderList = loader.SafeLoaderList([], "Chronos", self.__fresh_omsi_files())
        super().__init__(
            [
                self._global_config,
                self._tiles,
                self._standard_timetable,
                self._ailists,
                self._chronos,
            ],
            self.directory,# safe loader name
            self._files,
        )
    
    def load(self) -> None:
        self._files.set_omsi_files(self.__fresh_omsi_files())
        super().load()
    
    def get_directory(self):
        return self.directory
    
    def fully_loaded(self):
        return False#może kiedyś bedzie lepiej
    
    def get_global_config(self):
        return self._global_config
    
    def get_standard_timetable(self):
        return self._standard_timetable
    
    def get_ailists(self):
        return self._ailists
    
    def get_tiles(self):
        return self._tiles
    
    def get_chrono(self):
        return self._chronos

    def save_global_config(self):
        _global_config_serializer.serialize(self._global_config.get_data(), os.path.join(self.directory, GLOBAL_CONFIG_FILENAME))
    
    def save_tile(self, index):
        gc_tile = self._global_config._map[index]
        file_name = gc_tile.map_file
        print("Serializing tile file " + os.path.join(self.directory, file_name))
        _tile_serializer.serialize(self._tiles[index].get_data(), os.path.join(self.directory, file_name))
        self._tiles[index].save_files(self.directory)
    
    def save_tiles(self):
        for tile_index in range(len(self._global_config._map)):
            self.save_tile(tile_index)
    
    def __fresh_omsi_files(self) -> list[omsi_files.OmsiFile]:
        of_list = []
        for f in ["drivers.txt",
                  "Holidays.txt",
                  "humans.txt",
                  "parklist_p.txt",
                  "registrations.txt",
                  "signalroutes.cfg",
                  "texture/water.tga",
                  "texture/water_bump.bmp",
                  "texture/water_envmap.bmp",
                  "unsched_trafficdens.txt",
                  "unsched_vehgroups.txt"
                  ]:
            of_list.append(omsi_files.OmsiFile(map_path=self.directory, pattern=f))
        for f in ["picture.jpg",
                  "timezone.txt",
                  ]:
            of_list.append(omsi_files.OmsiFile(map_path=self.directory, pattern=f, optional=True))
        for f in [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Holidays_*.txt"))]:
            of_list.append(omsi_files.OmsiFile(map_path=self.directory, pattern=f, optional=True))
        return of_list
    
    def save_files(self):
        self._files.save(self.directory)
    
    def save_standard_timetable(self):
        self._standard_timetable.save()
    
    def save_ailists(self):
        print("Serializing ailists file " + os.path.join(self.directory, AILISTS_FILENAME))
        _ailists_serializer.serialize(self._ailists, os.path.join(self.directory, AILISTS_FILENAME))
    
    def scan_chrono(self):
        chrono_directory_list = [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Chrono", "*", ""))]
        self._chronos.set_data([chrono.Chrono(self.directory, chrono_directory, self._global_config.get_data()._map) for chrono_directory in chrono_directory_list])
    
    def save_chrono(self):
        for chrono in self._chronos:
            chrono.save(self.directory)
        
    def save(self):
        pathlib.Path(os.path.join(self.directory, "texture", "map")).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(self.directory, "TTData")).mkdir(parents=True, exist_ok=True)
        self.save_global_config()
        self.save_tiles()
        self.save_files()
        self.save_standard_timetable()
        self.save_ailists()
        self.save_chrono()
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        for tile_index, til in self._tiles.items():
            print("Changing objects' IDs and splines' IDs: TILE " + str(tile_index))
            til.change_ids(ids_value)
        
        self._standard_timetable.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
        
        print("Changing entrypoints' IDs and tile indexes: global_config")
        self._global_config.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
        
        for chrono in self._chronos:
            chrono.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
    
    def change_groundtex_indexes(self, value):
        for tile_index, til in self._tiles.items():
            til.change_groundtex_indexes(value)
