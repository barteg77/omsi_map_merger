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
import itertools
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
import logging
import typing

logger = logging.getLogger(__name__)

GLOBAL_CONFIG_FILENAME = "global.cfg"
AILISTS_FILENAME = "ailists.cfg"

_global_config_parser = global_config_parser.GlobalConfigParser()
_global_config_serializer = global_config_serializer.GlobalConfigSerializer()

_tile_parser = tile_parser.TileParser()
_tile_serializer = tile_serializer.TileSerializer()

_ailists_parser = ailists_parser.AIListsParser()
_ailists_serializer = ailists_serializer.AIListsSerializer()

class OmsiMap:
    def __init__(self,
                 mglobal_config: global_config.GlobalConfig,
                 mtiles: list[tile.Tile],
                 momsi_files: omsi_files.OmsiFiles,
                 mstandard_timetable: timetable.Timetable,
                 mailists: ailists.AILists,
                 mchronos: list[chrono.Chrono],
    ):
        self.global_config: global_config.GlobalConfig = mglobal_config
        self.tiles: list[tile.Tile] = mtiles
        self.mfiles: omsi_files.OmsiFiles = momsi_files
        self.mstandard_timetable: timetable.Timetable = mstandard_timetable
        self.ailists: ailists.AILists = mailists
        self.mchronos: list[chrono.Chrono] = mchronos
    
    def shift_ids(self, value: int) -> None:
        for mtile in self.tiles:
            mtile.change_ids(value)
    
    def change_ids_and_tile_indices(self, ids_value: int, tile_indices_value: int) -> None:
        for tile_index, til in zip(itertools.count(), self.tiles):
            logger.info(f"Changing objects' IDs and splines' IDs: TILE {tile_index}")
            til.change_ids(ids_value)
        
        self.mstandard_timetable.change_ids_and_tile_indices(ids_value, tile_indices_value)
        
        logger.info("Changing entrypoints' IDs and tile indices: global_config")
        self.global_config.change_ids_and_tile_indices(ids_value, tile_indices_value)
        
        for chrono in self.mchronos:
            chrono.change_ids_and_tile_indices(ids_value, tile_indices_value)
    
    def change_groundtex_indices(self, value: int) -> None:
        for til in self.tiles:
            til.change_groundtex_indices(value)
    
    def save_tiles(self, directory: str) -> None:
        for gc_tile, map_tile in zip(self.global_config._map, self.tiles):
            _tile_serializer.serialize(map_tile, os.path.join(directory, gc_tile.map_file))
            map_tile.save_files(directory)
    
    def get_time_table_line_names(self) -> list[str]:
        return list(set(itertools.chain.from_iterable([tt.get_time_table_line_names() for tt in [self.mstandard_timetable] + [mchrono.timetable for mchrono in self.mchronos]])))
    
    def get_tracks_names(self) -> list[str]:
        return list(set(itertools.chain.from_iterable([tt.get_tracks_names() for tt in [self.mstandard_timetable] + [mchrono.timetable for mchrono in self.mchronos]])))
    
    def get_trips_names(self) -> list[str]:
        return list(set(itertools.chain.from_iterable([tt.get_trips_names() for tt in [self.mstandard_timetable] + [mchrono.timetable for mchrono in self.mchronos]])))
    
    def save(self, directory: str) -> None:
        #prepare directories
        logger.info(f"Saving OmsiMap to directory: \"{directory}\"")
        logger.info(f"Will create \"{directory}\" directory if not exists")
        os.makedirs(directory, exist_ok=True)
        if os.listdir(directory) != []:
            raise Exception(f"Directory \"{directory}\" isn't empty.\nYou can save map only to empty directory.")
        os.makedirs(os.path.join(directory, 'texture', 'map'))
        
        _global_config_serializer.serialize(self.global_config, os.path.join(directory, GLOBAL_CONFIG_FILENAME))
        self.save_tiles(directory)
        self.mfiles.save(directory)
        self.mstandard_timetable.save(directory)
        _ailists_serializer.serialize(self.ailists, os.path.join(directory, AILISTS_FILENAME))
        for chrono in self.mchronos:
            chrono.save(directory)
        logger.info("Map saving completed")

class TileOFInjector:
    def __init__(self,
                 parser: typing.Callable[[str], tile.Tile],
                 of: omsi_files.OmsiFiles) -> None:
        self.parser: typing.Callable[[str], tile.Tile] = parser
        self.of: omsi_files.OmsiFiles = of
    
    def parse(self, path: str) -> tile.Tile:
        parsed_tile: tile.Tile = self.parser(path)
        parsed_tile._files = self.of
        return parsed_tile
    
class OmsiMapSl(loader.SafeLoaderList):
    def set_tiles_and_chronos_gc_consistent(self) -> None:
        self.empty_tiles_and_chronos()
        # set tiles' safe parsers
        tiles_safe_loaders: list[loader.SafeLoader] = []
        groundtex_count: int = len(self._global_config.get_data().groundtex)
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
                                      params={"pos_x": gc_tile.pos_x, "pos_y": gc_tile.pos_y, "groundtex_index": str(groundtex_index)},
                                      optional=True)
                  for groundtex_index in range(1, groundtex_count+1) ])
            tiles_safe_loaders.append(loader.SafeLoaderUnit(tile.Tile, os.path.join(self.directory, gc_tile.map_file), TileOFInjector(_tile_parser.parse, tile_files).parse , ofiles=tile_files))
        self._tiles.set_sl_list(tiles_safe_loaders)
        self.scan_chrono()
    
    def empty_tiles_and_chronos(self) -> None:
        self._tiles.set_sl_list([])
        self._chronos.set_sl_list([])

    def __init__(self,
                 directory=""):
        self.directory = directory
        self._global_config: loader.SafeLoaderUnit[global_config.GlobalConfig] = loader.SafeLoaderUnit(global_config.GlobalConfig,
                                                                           os.path.join(self.directory, GLOBAL_CONFIG_FILENAME),
                                                                           _global_config_parser.parse,
                                                                           self.set_tiles_and_chronos_gc_consistent, # on success
                                                                           self.empty_tiles_and_chronos, # on fail
                                                                           )
        self._tiles: loader.SafeLoaderList = loader.SafeLoaderList([], "Tiles")
        self._files: omsi_files.OmsiFiles = omsi_files.OmsiFiles(self.__fresh_omsi_files())
        self._standard_timetable: timetable.TimetableSl = timetable.TimetableSl(self.directory)
        self._ailists: loader.SafeLoaderUnit = loader.SafeLoaderUnit(ailists.AILists, os.path.join(self.directory, AILISTS_FILENAME), _ailists_parser.parse)
        self._chronos: loader.SafeLoaderList = loader.SafeLoaderList([], "Chronos")
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
    
    def get_global_config(self) -> loader.SafeLoaderUnit[global_config.GlobalConfig]:
        return self._global_config
    
    def get_standard_timetable(self):
        return self._standard_timetable
    
    def get_ailists(self) -> loader.SafeLoaderUnit[ailists.AILists]:
        return self._ailists
    
    def get_tiles(self):
        return self._tiles
    
    def get_chrono(self) -> loader.SafeLoaderList:
        return self._chronos

    def save_global_config(self):
        _global_config_serializer.serialize(self._global_config.get_data(), os.path.join(self.directory, GLOBAL_CONFIG_FILENAME))
    
    def __fresh_omsi_files(self) -> list[omsi_files.OmsiFile]:
        of_list: list[omsi_files.OmsiFile] = []
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

    def scan_chrono(self):
        chrono_directory_list = [os.path.relpath(x, self.directory) for x in glob.glob(os.path.join(self.directory, "Chrono", "*", ""))]
        self._chronos.set_sl_list([chrono.ChronoSl(self.directory, chrono_directory, self._global_config.get_data()._map) for chrono_directory in chrono_directory_list])
    
    def get_aigroups_names(self) -> list[str]:
        return [aigroup.name for aigroup in self.get_ailists().get_data().aigroups]
    
    def get_data(self) -> OmsiMap:
        if not self.ready():
            raise loader.NoDataError
        return OmsiMap(self.get_global_config().get_data(),
                       [typing.cast(loader.SafeLoaderUnit[tile.Tile], tile_sl).get_data() for tile_sl in self.get_tiles().get_sl_list()],
                       self.get_omsi_files(),
                       self.get_standard_timetable().get_data(),
                       self.get_ailists().get_data(),
                       [typing.cast(chrono.ChronoSl, x).get_data() for x in self.get_chrono().get_sl_list()])
