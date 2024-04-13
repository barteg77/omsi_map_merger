# Copyright 2020, 2023, 2024 Bartosz Gajewski
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

import global_config
import chrono_tile
import chrono_tile_parser
import chrono_tile_serializer
import timetable
import omsi_files
import os
import glob
import pathlib
import loader

_chrono_tile_parser = chrono_tile_parser.ChronoTileParser()
_chrono_tile_serializer = chrono_tile_serializer.ChronoTileSerializer()

class ChronoTileLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path, "ttl")
        self.data: chrono_tile.ChronoTile = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data = _chrono_tile_parser.parse(self.path)

class ChronoTileInfo:
    def __init__(self,
                 directory,
                 pos_x,
                 pos_y,
                 tile=None
                 ):
        self.directory = directory
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile = tile

class Chrono:
    def __init__(self,
                 map_directory: str,
                 chrono_directory: str,
                 gc_map: list[global_config.Map],
                 ):
        self.map_directory: str = map_directory
        self.chrono_directory: str = chrono_directory
        self.gc_map: list[global_config.Map] = gc_map
        self.chrono_config = None
        self.chrono_translations = omsi_files.OmsiFiles()
        self.chrono_tiles: list[loader.SafeLoader] = list(map(lambda tile: loader.SafeLoader(ChronoTileLoader(os.path.join(map_directory, self.chrono_directory, tile.map_file)), optional=True), self.gc_map))
        self.chrono_tiles_infos = []
        self.timetable: timetable.Timetable = timetable.Timetable(os.path.join(self.map_directory, self.chrono_directory))
    
    def get_timetable(self):
        return self.timetable
    
    def get_chrono_tiles(self):
        return self.chrono_tiles
    
    def load(self):
        self.chrono_config = omsi_files.OmsiFile(map_path=self.map_directory, pattern=os.path.join(self.chrono_directory, "Chrono.cfg"))
        for f in [os.path.relpath(x, self.map_directory) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "Chrono_*.dsc"))]:
            self.chrono_translations.add(omsi_files.OmsiFile(map_path=self.map_directory, pattern=f, optional=True))
        
        # HERE LOAD EVERY CHRONO TILE
        self.get_timetable().load()
    
    def save(self,
             map_directory
             ):
        pathlib.Path(os.path.join(map_directory, self.chrono_directory, "TTData")).mkdir(parents=True, exist_ok=True)
        self.chrono_config.save(map_directory)
        self.chrono_translations.save(map_directory)
        for chrono_tile in self.chrono_tiles_infos:
            print("Serializing chrono tile file " + os.path.join(map_directory, chrono_tile.directory, "tile_"+chrono_tile.pos_x+"_"+chrono_tile.pos_y+".map"))
            _chrono_tile_serializer.serialize(chrono_tile.tile, os.path.join(map_directory, chrono_tile.directory, "tile_"+chrono_tile.pos_x+"_"+chrono_tile.pos_y+".map"))
        self.timetable.save(map_directory)
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        for chrono_tiles_info in self.chrono_tiles_infos:
            chrono_tiles_info.tile.change_ids(ids_value)
        self.timetable.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
