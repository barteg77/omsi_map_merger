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
import tile
import ailists
import timetable
import os
import typing
import itertools
import operator
import version
import copy
import logging

logger = logging.getLogger(__name__)

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

class MapToMerge(omsi_map.OmsiMapSl):
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
    
    def __repr__(self) -> str:
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
    
    def set_keep_groundtex(self, value: bool) -> None:
        self.__keep_groundtex = value
    
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

def tile_shifted_ids(tile_old: tile.Tile, id_shift: int) -> tile.Tile:
    new_splines: list[tile.Spline] =  [tile.Spline(s.h, s.line1, s.file_name, s.id+id_shift, s.id_previous+id_shift if s.id_previous!=0 else 0, s.id_next+id_shift if s.id_next!=0 else 0, \
                                                   s.pos_x, s.pos_z, s.pos_y, s.rotate, s.length, s.radius, \
                                                   s.gradient_start, s.gradient_end, s.delta_h, s.cant_start, s.cant_end, s.skew_start, \
                                                   s.skew_end, s.line18, s.mirror, s.spline_terrain_align_2, s.rule_list) \
                                        for s in tile_old.spline]
    
    def sceneryobject_id_shifted(sco) -> tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater: # type: ignore
        def son(sco_id: int | None, shift: int) -> int | None:
            return None if sco_id is None else sco_id+shift
        sco_type: typing.Type[tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater] = type(sco)
        match sco_type:
            case tile._Object:
                return tile._Object(sco.description, sco.attach_object, sco.line1, sco.file_name, sco.id+id_shift, sco.pos_x, \
                                    sco.pos_z, sco.pos_y, sco.rotate, sco.pitch, sco.bank, sco.line10, \
                                        sco.opt_lines, son(sco.varparent, id_shift), sco.spline_terrain_align, sco.rule_list)
            case tile.SplineAttachement:
                return tile.SplineAttachement(sco.description, sco.line1, sco.file_name, sco.id+id_shift, sco.line4, sco.pos_x, \
                                              sco.pos_z, sco.pos_y, sco.rotate, sco.pitch, sco.bank, sco.interval, \
                                              sco.distance, sco.line13, sco.line14, sco.opt_lines, son(sco.varparent, id_shift), sco.spline_terrain_align, \
                                              sco.rule_list)
            case tile.SplineAttachementRepeater:
                return tile.SplineAttachementRepeater(sco.description, sco.line1, sco.line2, sco.line3, sco.file_name, sco.id+id_shift, \
                                                      sco.line6, sco.pos_x, sco.pos_z, sco.pos_y, sco.rotate, sco.pitch, \
                                                      sco.bank, sco.interval, sco.distance, sco.line15, sco.line16, sco.opt_lines, \
                                                      son(sco.varparent, id_shift), sco.spline_terrain_align, sco.rule_list)
    
    return tile.Tile(tile_old.initial_comment,
                     tile_old.version,
                     tile_old.terrain,
                     tile_old.water,
                     tile_old.variable_terrainlightmap,
                     tile_old.variable_terrain,
                     new_splines,
                     list(map(sceneryobject_id_shifted, tile_old._object)))

class MergeResult:
    def __init__(self,
                 merged_map: omsi_map.OmsiMap,
                 warnings: list[str]):
        self.merged_map: omsi_map.OmsiMap = merged_map
        self.warnings: list[str] = warnings

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
    
    def aigroup_name_collision(self) -> bool:
        aigroups_names_seq: list[str] = list(itertools.chain.from_iterable([[aig.name for aig in mtm.get_ailists().get_data().aigroups] for mtm in self.get_maps()]))
        return len(set(aigroups_names_seq)) != len(aigroups_names_seq)
    
    def ready(self) -> bool:
        return all([mtm.ready() for mtm in self.get_maps()]) and not self.overlapping() and len(self.get_maps()) >= 2
    
    def merged_gc_groundtex(self) -> list[global_config.GroundTex]:
        assert not self.get_maps()[0].get_keep_groundtex()
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

    def merged_omsi_map(self, new_map_name: str) -> MergeResult:
        assert self.ready(), "You can't get merged omsi map while not all maps are ready"
        assert not self.get_maps()[0].get_keep_groundtex(), "\"Keep groundtex\" on 1st map is nonsense."

        # warnings about merged map
        warns: list[str] = []
        def warn(message: str) -> None:
            logger.info(f"Map merge warning reported: {message}")
            warns.append(message)
        
        # warning about empty map name
        if new_map_name == "":
            warn("Map name is empty")
        
        # warning about aigroup name collision
        if self.aigroup_name_collision():
            warn("Aigroup name collision")
        
        fm: dict[MapToMerge, omsi_map.OmsiMap] = dict([(mtm, copy.deepcopy(mtm.get_data())) for mtm in self.get_maps()])

        # warning about set worldcoordinates
        for mtm in self.get_maps():
            if fm[mtm].global_config.worldcoordinates:
                warn(f"[worldcoordinates] are set in \"{mtm.get_directory}\" map global.cfg. \
                     This WILL cause corruption of merged map. (This program is not capable of merging maps with set worldcoordinates.)")
        
        # warning about ttl, ttp, ttr names collision
        for tt_entity_name_plural, names_list_list in [
            ("lines (ttl)", [fm[mtm].get_time_table_line_names() for mtm in self.get_maps()]),
            ("tracks (ttr)", [fm[mtm].get_tracks_names() for mtm in self.get_maps()]),
            ("trips (ttp)", [fm[mtm].get_trips_names() for mtm in self.get_maps()]),
        ]:
            names: list[str] = list(itertools.chain.from_iterable(names_list_list))
            if len(names) != len(set(names)):
                warn(f"Time table {tt_entity_name_plural} names collision")

        idcode_shift: dict[MapToMerge, int] = self.merged_idcodes_shifts()
        tile_shift: dict[MapToMerge, int] = self.merged_tiles_indices_shift()
        groundtex_shift: dict[MapToMerge, int] = self.merged_groundtex_shift()
        
        # print shifts debug log
        for name, shift_dict in [
            ("IDCode",idcode_shift),
            ("Tile", tile_shift),
            ("Groundtex", groundtex_shift),
        ]:
            logger.debug(f"Calculated {name} shift: {shift_dict}")

        comment: str = f"File created with OMSI Map Merger {version.version}"

        # constructing global config
        map_description: str = f"{new_map_name}\nMap created with OMSI Map Merger {version.version}\nMerged maps (path, shift_x, shift_y, keep_groundtex):\n"\
        + "".join(["\n* " + ", ".join([mtm.get_directory(), str(mtm.get_shift_x()), str(mtm.get_shift_y()), str(mtm.get_keep_groundtex())]) for mtm in self.get_maps()])
        
        gc_entrypoints: list[global_config.Entrypoints] = list(itertools.chain.from_iterable([shifted_entrypoints(fm[mtm].global_config.entrypoints,
                                                                                                                  idcode_shift[mtm],
                                                                                                                  tile_shift[mtm]) for mtm in self.get_maps()]))
        gc_tiles: list[global_config.Map] = list(itertools.chain.from_iterable([shifted_gc_tiles(fm[mtm].global_config._map,
                                                                                                 mtm.get_shift_x(),
                                                                                                 mtm.get_shift_y()) for mtm in self.get_maps()]))
        gc: global_config.GlobalConfig
        gc = global_config.GlobalConfig(comment,
                                        new_map_name,
                                        new_map_name,
                                        map_description.split("\n"),
                                        '14',
                                        sum([mtm.get_global_config().get_data().NextIDCode for mtm in self.get_maps()]),
                                        False,
                                        False,
                                        False,
                                        fm[self.get_maps()[0]].global_config.backgroundimage,
                                        fm[self.get_maps()[0]].global_config.mapcam,
                                        fm[self.get_maps()[0]].global_config.moneysystem,
                                        fm[self.get_maps()[0]].global_config.ticketpack,
                                        fm[self.get_maps()[0]].global_config.repair_time_min,
                                        fm[self.get_maps()[0]].global_config.years,
                                        fm[self.get_maps()[0]].global_config.realyearoffset,
                                        fm[self.get_maps()[0]].global_config.standarddepot,
                                        self.merged_gc_groundtex(),
                                        fm[self.get_maps()[0]].global_config.addseason,
                                        fm[self.get_maps()[0]].global_config.trafficdensity_road,
                                        fm[self.get_maps()[0]].global_config.trafficdensity_passenger,
                                        gc_entrypoints,
                                        gc_tiles,
                                        )
        
        # shift idcodes, tile indices, groundtex indices
        for mtm in self.get_maps():
            fm[mtm].change_ids_and_tile_indices(idcode_shift[mtm],  tile_shift[mtm])
            fm[mtm].change_groundtex_indices(groundtex_shift[mtm])
        
        # prepare tiles for merged map
        tiles: list[tile.Tile] = list(itertools.chain.from_iterable([fm[mtm].tiles for mtm in self.get_maps()]))
        for map_tile, gc_tile in zip(tiles, gc_tiles):
            map_tile.set_files_pos(gc_tile.pos_x, gc_tile.pos_y)
        
        new_om: omsi_map.OmsiMap = omsi_map.OmsiMap(gc,
                                                    tiles,
                                                    fm[self.get_maps()[0]].mfiles,
                                                    timetable.joined([fm[mtm].mstandard_timetable for mtm in self.get_maps()]),
                                                    ailists.AILists(list(itertools.chain.from_iterable([fm[mtm].ailists.aigroups for mtm in self.get_maps()]))),
                                                    list(itertools.chain.from_iterable([fm[mtm].mchronos for mtm in self.get_maps()])),
                                                    )
        logger.info("Maps merge completed")
        return MergeResult(new_om, warns)