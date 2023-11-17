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
import loader
from enum import Enum

GLOBAL_CONFIG_FILENAME = "global.cfg"
AILISTS_FILENAME = "ailists.cfg"

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


class GlobalConfigLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__() 
        self.data: global_config.GlobalConfig = None
        self.__path: str = path

    def load(self) -> None:
        self.data = _global_config_parser.parse(self.__path)

class TileLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__() 
        self.data: tile.Tile = None
        self.__path: str = path
    
    def load(self) -> None:
        self.data: tile.Tile = _tile_parser.parse(self.__path)

class TimetableLoader(loader.Loader):
    def __init__(self, parent_directory: str) -> None:
        super().__init__() 
        self.data: timetable.Timetable = None
        self.__path: str = parent_directory
    
    def load(self) -> None:
        self.data = timetable.Timetable()
        self.__data.load(self.__path)

class AilistsLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__() 
        self.data: ailists.AILists = None
        self.__path: str = path
    
    def load(self) -> None:
        self.data = _ailists_parser.parse(self.__path)

class ChronoLoader(loader.Loader):
    def __init__(self, directory: str, gc_map: list[global_config.Map]) -> None:
        super().__init__() 
        self.data: chrono.Chrono()
        self.__directory: str = directory
        self.__gc_map: list[global_config.Map] = gc_map
    
    def load(self) -> None:
        self.data = chrono.Chrono()
        self.data.load(self.__directory, self.__gc_map)

class SafeLoader:
    def __init__(self, real_loader) -> None:
        self.__real_loader: Loader = real_loader
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception: Exception = None
    
    def get_status(self) -> FileParsingStatus:
        return self.__status
    
    def get_data(self) -> None:
        if self.__status == FileParsingStatus.READ_SUCCESS:
            return self.__real_loader.data
        else:
            raise NoDataError(f"Unable to return data, file parsing status is {self.__status}.")
    
    def load(self) -> None:
        print(type(self.__real_loader).__name__, "loading file...")
        try:
            self.__real_loader.load()
            self.__status = FileParsingStatus.READ_SUCCESS
            self.__exception  = None
        except Exception as exception:
            self.__status = FileParsingStatus.ERROR
            self.__exception = exception
    
    def info_short(self) -> str:
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "NOT READ"
            case FileParsingStatus.READ_SUCCESS:
                return "READ SUCCESSFULLY"
            case FileParsingStatus.ERROR:
                return f"ERROR: {type(self.__exception).__name__}"
    
    def info_detailed(self) -> str:
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "File not read yet."
            case FileParsingStatus.READ_SUCCESS:
                return "Loaded successfully."
            case FileParsingStatus.ERROR:
                return str(self.__exception)

class OmsiMap:
    def __init__(self,
                 directory=""):
        self.directory = directory
        self._global_config: SafeLoader = SafeLoader(GlobalConfigLoader(os.path.join(self.directory, GLOBAL_CONFIG_FILENAME)))
        self._tiles: list[SafeLoader] = []
        self._files: omsi_files.OmsiFiles = omsi_files.OmsiFiles()
        self._standard_timetable: SafeLoader = SafeLoader(TimetableLoader(self.directory))
        self._ailists: SafeLoader = SafeLoader(AilistsLoader(os.path.join(self.directory, AILISTS_FILENAME)))
        self._chronos: list[SafeLoader] = []
    
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
    
    def load_global_config(self):# affects self._tiles too
        self._global_config.load()
        # set tiles' safe parsers
        if self._global_config.get_status() == FileParsingStatus.READ_SUCCESS:
            for gc_tile in self._global_config.get_data()._map:
                self._tiles.append(SafeLoader(TileLoader(os.path.join(self.directory, gc_tile.map_file))))#### to w innym miejscu musi być bo się 
                #                                                                               global config przeladowuje SafeLoaderem a nie tym

    def save_global_config(self):
        _global_config_serializer.serialize(self._global_config.get_data(), os.path.join(self.directory, GLOBAL_CONFIG_FILENAME))
    
    def load_tiles(self):
        for tile in self._tiles:
            tile.load()
    
    def save_tile(self, index):
        gc_tile = self._global_config._map[index]
        file_name = gc_tile.map_file
        print("Serializing tile file " + os.path.join(self.directory, file_name))
        _tile_serializer.serialize(self._tiles[index].get_data(), os.path.join(self.directory, file_name))
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
        self._standard_timetable.load()
    
    def save_standard_timetable(self):
        self._standard_timetable.save(self.directory)
    
    def load_ailists(self):
        self._ailists.load()
    
    def save_ailists(self):
        print("Serializing ailists file " + os.path.join(self.directory, AILISTS_FILENAME))
        _ailists_serializer.serialize(self._ailists, os.path.join(self.directory, AILISTS_FILENAME))
    
    def load_chrono(self):
        chrono_directory_list = [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Chrono", "*", ""))]
        for chrono_directory in chrono_directory_list:
            self._chronos.append(SafeLoader(ChronoLoader(os.path.join(self.directory, chrono_directory), self._global_config.get_data()._map)))
            self._chronos[-1].load()
    
    def save_chrono(self):
        for chrono in self._chronos:
            chrono.save(self.directory)
    
    def load(self):
        self.load_global_config()
        if self._global_config.get_status() == FileParsingStatus.READ_SUCCESS:
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
