# Copyright 2020, 2021, 2023 Bartosz Gajewski
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

_global_config_parser = global_config_parser.GlobalConfigParser()
_global_config_serializer = global_config_serializer.GlobalConfigSerializer()

_tile_parser = tile_parser.TileParser()
_tile_serializer = tile_serializer.TileSerializer()

_ailists_parser = ailists_parser.AIListsParser()
_ailists_serializer = ailists_serializer.AIListsSerializer()

class NoDataError(Exception):
    pass

class FileParsingStatus(Enum):
    NOT_READ = 1
    READ_SUCCESS = 2
    ERROR = 3

class GloalConfigOrError:
    def __init__(self):
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception = None
        self.__data: global_config.GlobalConfig = None
    
    def get_status(self):
        return self.__status
    
    def get_data(self):
        if self.__status == FileParsingStatus.READ_SUCCESS:
            return self.__data
        else:
            raise NoDataError(f"Unable to return data, file parsing status is {self.__status}."
    
    def load(self, path):
        try:
            self.__data = _global_config_parser.parse(path)
        except as exception:
            self.__status = FileParsingStatus.ERROR
            self.__exception = exception
    
    def info_short(self):
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "NOT READ"
            case FileParsingStatus.READ_SUCCESS:
                return "READ SUCCESSFULLY"
            case FileParsingStatus.ERROR:
                return f"ERROR: {type(self.__exception).__name__}"
    
    def info_detailed(self):
        return str(self.__exception)


class OmsiMap:
    def __init__(self,
                 directory=""):
        self.directory = directory
        self._global_config: GlobalConfigOrError = GlobalConfigOrError()
        self._tiles = {}
        self._files = omsi_files.OmsiFiles()
        self._standard_timetable = None
        self._ailists = None
        self._chronos = []
    
    def load_global_config(self):
        self._global_config = _global_config_parser.parse(os.path.join(self.directory, "global.cfg"))

    def save_global_config(self):
        _global_config_serializer.serialize(self._global_config, os.path.join(self.directory, "global.cfg"))
    
    def load_tile(self, index):
        gc_tile = self._global_config._map[index]
        file_name = gc_tile.map_file
        print("Parsing tile file " + os.path.join(self.directory, file_name))
        self._tiles[index] = _tile_parser.parse(os.path.join(self.directory, file_name))
        self._tiles[index].load_files(self.directory, gc_tile.pos_x, gc_tile.pos_y, len(self._global_config.groundtex))
    
    def load_tiles(self):
        for tile_index in range(len(self._global_config._map)):
            self.load_tile(tile_index)
    
    def save_tile(self, index):
        gc_tile = self._global_config._map[index]
        file_name = gc_tile.map_file
        print("Serializing tile file " + os.path.join(self.directory, file_name))
        _tile_serializer.serialize(self._tiles[index], os.path.join(self.directory, file_name))
        self._tiles[index].save_files(self.directory)
    
    def save_tiles(self):
        for tile_index in range(len(self._global_config._map)):
            self.save_tile(tile_index)
    
    def load_files(self):
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
            self._files.add(omsi_files.OmsiFile(map_path=self.directory, pattern=f))
        for f in ["picture.jpg",
                  "timezone.txt",
                  ]:
            self._files.add(omsi_files.OmsiFile(map_path=self.directory, pattern=f, optional=True))
        for f in [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Holidays_*.txt"))]:
            self._files.add(omsi_files.OmsiFile(map_path=self.directory, pattern=f, optional=True))
    
    def save_files(self):
        self._files.save(self.directory)
    
    def load_standard_timetable(self):
        self._standard_timetable = timetable.Timetable()
        self._standard_timetable.load(self.directory)
    
    def save_standard_timetable(self):
        self._standard_timetable.save(self.directory)
    
    def load_ailists(self):
        if os.path.isfile(os.path.join(self.directory, "ailists.cfg")):
            print("Parsing ailists file " + os.path.join(self.directory, "ailists.cfg"))
            self._ailists = _ailists_parser.parse(os.path.join(self.directory, "ailists.cfg"))
        else:
            print("Ailists file " + os.path.join(self.directory, "ailists.cfg") + " does not exist, will not be parsed.")
            self._ailsts = ailists.AILists()
    
    def save_ailists(self):
        print("Serializing ailists file " + os.path.join(self.directory, "ailists.cfg"))
        _ailists_serializer.serialize(self._ailists, os.path.join(self.directory, "ailists.cfg"))
    
    def load_chrono(self):
        chrono_directory_list = [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Chrono", "*", ""))]
        for chrono_directory in chrono_directory_list:
            self._chronos.append(chrono.Chrono(chrono_directory))
            self._chronos[-1].load(self.directory, self._global_config._map)
    
    def save_chrono(self):
        for chrono in self._chronos:
            chrono.save(self.directory)
    
    def load(self):
        self.load_global_config()
        self.load_tiles()
        self.load_files()
        self.load_standard_timetable()
        self.load_ailists()
        self.load_chrono()
        
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
