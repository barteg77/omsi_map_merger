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

import omsi_files

class Rule:
    def __init__(self,
                 kill: bool,
                 line1: str,
                 line2: str,
                 line3: str,
                 line4: str
                 ):
        self.kill: bool = kill
        self.line1: str = line1
        self.line2: str = line2
        self.line3: str = line3
        self.line4: str = line4
    
    def __key(self):
        return (self.kill, self.line1, self.line2, self.line3, self.line4)
    
    def __eq__(self, other: 'Rule') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class Spline:
    def __init__(self,
                 h: bool,
                 line1: str,
                 file_name: str,
                 id: int,
                 id_previous: int,
                 id_next: int,
                 pos_x: str,
                 pos_z: str,
                 pos_y: str,
                 rotate: str,
                 length: str,
                 radius: str,
                 gradient_start: str,
                 gradient_end: str,
                 delta_h: str | None,
                 cant_start: str,
                 cant_end: str,
                 skew_start: str,
                 skew_end: str,
                 line18: str,
                 mirror: bool,
                 spline_terrain_align_2: str | None,
                 rule_list: list[Rule] | None,
                 ):
        assert h ^ (delta_h is None)
        self.h: bool = h
        self.line1: str = line1
        self.file_name: str = file_name
        self.id: int = id
        self.id_previous: int = id_previous
        self.id_next: int = id_next
        self.pos_x: str = pos_x
        self.pos_z: str = pos_z
        self.pos_y: str = pos_y
        self.rotate: str = rotate
        self.length: str = length
        self.radius: str = radius
        self.gradient_start: str = gradient_start
        self.gradient_end: str = gradient_end
        self.delta_h: str | None = delta_h
        self.cant_start: str = cant_start
        self.cant_end: str = cant_end
        self.skew_start: str = skew_start
        self.skew_end: str = skew_end
        self.line18: str = line18
        self.mirror: bool = mirror
        self.spline_terrain_align_2: str | None = spline_terrain_align_2
        self.rule_list: list[Rule] | None = rule_list
    
    def __key(self):
        return (self.h, self.line1, self.file_name, self.id, self.id_previous, self.id_next, \
                self.pos_x, self.pos_z, self.pos_y, self.rotate, self.length, self.radius, \
                self.gradient_start, self.gradient_end, self.delta_h, self.cant_start, self.cant_end, self.skew_start, \
                self.skew_end, self.line18, self.mirror, self.spline_terrain_align_2, self.rule_list)
    
    def __eq__(self, other: 'Spline') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class _Object:
    def __init__(self,
                 description: str,
				 attach_object: bool,
                 line1: str,
                 file_name: str,
                 id: int,
                 pos_x: str,
                 pos_z: str,
                 pos_y: str,
                 rotate: str,
                 pitch: str,
                 bank: str,
                 line10: str,
                 opt_lines: list[str] | None,
                 varparent: int | None,
                 spline_terrain_align: bool,
                 rule_list: list[Rule] | None,
                 ):
        self.description: str = description
        self.attach_object: bool = attach_object
        self.line1: str = line1
        self.file_name: str = file_name
        self.id: int = id
        self.pos_x: str = pos_x
        self.pos_z: str = pos_z
        self.pos_y: str = pos_y
        self.rotate: str = rotate
        self.pitch: str = pitch
        self.bank: str = bank
        self.line10: str = line10
        self.opt_lines: list[str] | None = opt_lines
        self.varparent: int | None = varparent
        self.spline_terrain_align: bool = spline_terrain_align
        self.rule_list: list[Rule] | None = rule_list
    
    def __key(self):
        return (self.description, self.attach_object, self.line1, self.file_name, self.id, self.pos_x, \
                self.pos_z, self.pos_y, self.rotate, self.pitch, self.bank, self.line10, \
                self.opt_lines, self.varparent, self.spline_terrain_align, self.rule_list)
    
    def __eq__(self, other: '_Object') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class SplineAttachement:
    def __init__(self,
                 description: str,
                 line1: str,
                 file_name: str,
                 id: int,
                 line4: str,
                 pos_x: str,
                 pos_z: str,
                 pos_y: str,
                 rotate: str,
                 pitch: str,
                 bank: str,
                 interval: str,
                 distance: str,
                 line13: str,
                 line14: str,
                 opt_lines: list[str] | None,
                 varparent: int | None,
                 spline_terrain_align: bool,
                 rule_list: list[Rule] | None,
                 ):
        self.description: str = description
        self.line1: str = line1
        self.file_name: str = file_name
        self.id: int = id
        self.line4: str = line4
        self.pos_x: str = pos_x
        self.pos_z: str = pos_z
        self.pos_y: str = pos_y
        self.rotate: str = rotate
        self.pitch: str = pitch
        self.bank: str = bank
        self.interval: str = interval
        self.distance: str = distance
        self.line13: str = line13
        self.line14: str = line14
        self.opt_lines: list[str] | None = opt_lines
        self.varparent: int | None = varparent
        self.spline_terrain_align: bool = spline_terrain_align
        self.rule_list: list[Rule] | None = rule_list
    
    def __key(self):
        return (self.description, self.line1, self.file_name, self.id, self.pos_x, self.pos_z, \
                self.pos_y, self.rotate, self.pitch, self.bank, self.interval, self.distance, \
                self.line13, self.line14, self.opt_lines, self.varparent, self.spline_terrain_align, self.rule_list)
    
    def __eq__(self, other: 'SplineAttachement') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class SplineAttachementRepeater:
    def __init__(self,
                 description: str,
                 line1: str,
                 line2: str,
                 line3: str,
                 file_name: str,
                 id: int,
                 line6: str,
                 pos_x: str,
                 pos_z: str,
                 pos_y: str,
                 rotate: str,
                 pitch: str,
                 bank: str,
                 interval: str,
                 distance: str,
                 line15: str,
                 line16: str,
                 opt_lines: list[str] | None,
                 varparent: int | None,
                 spline_terrain_align: bool,
                 rule_list: list[Rule] | None,
                 ):
        self.description: str = description
        self.line1: str = line1
        self.line2: str = line2
        self.line3: str = line3
        self.file_name: str = file_name
        self.id: int = id
        self.line6: str = line6
        self.pos_x: str = pos_x
        self.pos_z: str = pos_z
        self.pos_y: str = pos_y
        self.rotate: str = rotate
        self.pitch: str = pitch
        self.bank: str = bank
        self.interval: str = interval
        self.distance: str = distance
        self.line15: str = line15
        self.line16: str = line16
        self.opt_lines: list[str] | None = opt_lines
        self.varparent: int | None = varparent
        self.spline_terrain_align: bool = spline_terrain_align
        self.rule_list: list[Rule] | None = rule_list
    
    def __key(self):
        return (self.description, self.line1, self.line3, self.file_name, self.id, self.pos_x, \
                self.pos_z, self.pos_y, self.rotate, self.pitch, self.bank, self.interval, self.distance, \
                self.line15, self.line16, self.opt_lines, self.varparent, self.spline_terrain_align, self.rule_list)
    
    def __eq__(self, other: 'SplineAttachementRepeater') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())

class Tile:
    def __init__(self,
                 initial_comment: str,
                 version: str,
                 terrain: bool,
                 water: bool,
                 variable_terrainlightmap: bool,
                 variable_terrain: bool,
                 spline: list[Spline],
                 _object: list[_Object | SplineAttachement | SplineAttachementRepeater],
                 ):
        self.initial_comment: str = initial_comment
        self.version: str = version
        self.terrain: bool = terrain
        self.water: bool = water
        self.variable_terrainlightmap: bool = variable_terrainlightmap
        self.variable_terrain: bool = variable_terrain
        self.spline: list[Spline] = spline
        self._object: list[_Object | SplineAttachement | SplineAttachementRepeater] = _object
    
    def __key(self):
        return (self.initial_comment, self.version, self.terrain, self.water, self.variable_terrainlightmap, self.variable_terrain, \
                self.spline, self._object)
    
    def __eq__(self, other: 'Tile') -> bool:
        return self.__key() == other.__key()
    
    def __hash__(self) -> int:
        return hash(self.__key())