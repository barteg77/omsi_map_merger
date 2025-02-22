# Copyright 2020, 2023, 2024, 2025 Bartosz Gajewski
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

import typing

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
import logging

logger = logging.getLogger(__name__)

CHRONO_DIRNAME: str = 'Chrono'

_chrono_tile_parser = chrono_tile_parser.ChronoTileParser()
_chrono_tile_serializer = chrono_tile_serializer.ChronoTileSerializer()

class Chrono:
    def __init__(self,
                 chrono_directory: str,
                 chrono_tiles: dict[str, chrono_tile.ChronoTile], # only tiles with chrono tile
                 comsi_files: omsi_files.OmsiFiles,
                 ctimetable: timetable.Timetable,
    ):
        self.chrono_directory: str = chrono_directory
        self.chrono_tiles: dict[str, chrono_tile.ChronoTile] = chrono_tiles # only tiles with chrono tile
        self.omsi_files: omsi_files.OmsiFiles = comsi_files
        self.timetable: timetable.Timetable = ctimetable
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int) -> None:
        for chrono_file_name in self.chrono_tiles:
            self.chrono_tiles[chrono_file_name].change_ids(ids_value)
        self.timetable.change_ids_and_tile_indices(ids_value, tile_indices_value)
    
    def save(self, map_directory: str) -> None:
        joined_directory: str = os.path.join(map_directory, self.chrono_directory)
        pathlib.Path(joined_directory).mkdir(parents=True)
        self.omsi_files.save(map_directory)
        for chrono_file_name in self.chrono_tiles:
            file_path: str = os.path.join(joined_directory, chrono_file_name)
            logger.info(f"Serializing chrono tile file {file_path}...")
            _chrono_tile_serializer.serialize(self.chrono_tiles[chrono_file_name], file_path)
        self.timetable.save(joined_directory)

class ChronoSl(loader.SafeLoaderList):
    def __init__(self,
                 map_directory: str,
                 chrono_directory: str,
                 tiles_filenames: set[str]
                 ):
        self.map_directory: str = map_directory
        self.chrono_directory: str = chrono_directory
        self.chrono_translations = omsi_files.OmsiFiles()
        self.chrono_tiles: loader.SafeLoaderList = loader.SafeLoaderList(list(map(lambda tile_filename: loader.SafeLoaderUnit(chrono_tile.ChronoTile, os.path.join(map_directory, self.chrono_directory, tile_filename), _chrono_tile_parser.parse, optional=True), tiles_filenames)), "Chrono tiles")
        self.timetable: timetable.TimetableSl = timetable.TimetableSl(os.path.join(self.map_directory, self.chrono_directory))
        super().__init__([self.chrono_tiles, self.timetable],
                         self.chrono_directory,
                         omsi_files.OmsiFiles(self.__all_omsi_files()),
                         )
    
    def __lang_files_names(self):
        return [os.path.relpath(x, self.map_directory) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "Chrono_*.dsc"))]
    
    def __all_files_names(self):
        return [os.path.join(self.chrono_directory, "Chrono.cfg")] + self.__lang_files_names()
    
    def __all_omsi_files(self):
        return [omsi_files.OmsiFile(self.map_directory, file_name) for file_name in self.__all_files_names()]

    def get_timetable(self):
        return self.timetable
    
    def get_chrono_tiles(self):
        return self.chrono_tiles
    
    def load(self):
        super().get_omsi_files().set_omsi_files(self.__all_omsi_files())
        super().load()
        self.get_timetable().load()
    
    def get_data(self) -> Chrono:
        if not self.ready():
            raise loader.NoDataError
        chrono_tiles: dict[str, chrono_tile.ChronoTile] = dict((sl.get_filename(), sl.get_data())
                                                               for sl
                                                               in map(lambda asl: typing.cast(loader.SafeLoaderUnit[chrono_tile.ChronoTile], asl), self.chrono_tiles.get_sl_list())
                                                               if sl.get_status() != loader.FileParsingStatus.OPTIONAL_NOT_EXISTS
                                                               )
        return Chrono(self.chrono_directory, chrono_tiles, self.get_omsi_files(), self.get_timetable().get_data())