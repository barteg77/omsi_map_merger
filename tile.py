# Copyright 2020, 2023 Bartosz Gajewski
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

class Spline:
    def __init__(self,
                 h=False,
                 line1=None,
                 file_name=None,
                 id=None,
                 id_previous=None,
                 id_next=None,
                 pos_x=None,
                 pos_z=None,
                 pos_y=None,
                 rotate=None,
                 length=None,
                 radius=None,
                 gradient_start=None,
                 gradient_end=None,
                 delta_h=None,
                 cant_start=None,
                 cant_end=None,
                 skew_start=None,
                 skew_end=None,
                 line18=None,
                 mirror=False,
                 spline_terrain_align_2=None,
                 rule_list=[]
                 ):
        self.h = h
        self.line1 = line1
        self.file_name = file_name
        self.id = id
        self.id_previous = id_previous
        self.id_next = id_next
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.pos_y = pos_y
        self.rotate = rotate
        self.length = length
        self.radius = radius
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end
        self.delta_h = delta_h
        self.cant_start = cant_start
        self.cant_end = cant_end
        self.skew_start = skew_start
        self.skew_end = skew_end
        self.line18 = line18
        self.mirror = mirror
        self.spline_terrain_align_2 = spline_terrain_align_2
        self.rule_list = rule_list

class _Object:
    def __init__(self,
                 description=None,
				 attach_object=False,
                 line1=None,
                 file_name=None,
                 id=None,
                 pos_x=None,
                 pos_z=None,
                 pos_y=None,
                 rotate=None,
                 pitch=None,
                 bank=None,
                 line10=None,
                 opt_lines=[],
                 varparent=None,
                 spline_terrain_align=False,
                 rule_list=[]
                 ):
        self.description = description
        self.attach_object = attach_object
        self.line1 = line1
        self.file_name = file_name
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.rotate = rotate
        self.pitch = pitch
        self.bank = bank
        self.line10 = line10
        self.opt_lines = opt_lines
        self.varparent = varparent
        self.spline_terrain_align = spline_terrain_align
        self.rule_list = rule_list

class SplineAttachement:
    def __init__(self,
                 description=None,
                 line1=None,
                 file_name=None,
                 id=None,
                 line4=None,
                 pos_x=None,
                 pos_z=None,
                 pos_y=None,
                 rotate=None,
                 pitch=None,
                 bank=None,
                 interval=None,
                 distance=None,
                 line13=None,
                 line14=None,
                 opt_lines=[],
                 varparent=None,
                 spline_terrain_align=False,
                 rule_list=None,
                 ):
        self.description = description
        self.line1 = line1
        self.file_name = file_name
        self.id = id
        self.line4 = line4
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.pos_y = pos_y
        self.rotate = rotate
        self.pitch = pitch
        self.bank = bank
        self.interval = interval
        self.distance = distance
        self.line13 = line13
        self.line14 = line14
        self.opt_lines = opt_lines
        self.varparent = varparent
        self.spline_terrain_align = spline_terrain_align
        self.rule_list = rule_list

class SplineAttachementRepeater:
    def __init__(self,
                 description=None,
                 line1=None,
                 line2=None,
                 line3=None,
                 file_name=None,
                 id=None,
                 line6=None,
                 pos_x=None,
                 pos_z=None,
                 pos_y=None,
                 rotate=None,
                 pitch=None,
                 bank=None,
                 interval=None,
                 distance=None,
                 line15=None,
                 line16=None,
                 opt_lines=[],
                 varparent=None,
                 spline_terrain_align=False,
                 rule_list=[]
                 ):
        self.description = description
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.file_name = file_name
        self.id = id
        self.line6 = line6
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.pos_y = pos_y
        self.rotate = rotate
        self.pitch = pitch
        self.bank = bank
        self.interval = interval
        self.distance = distance
        self.line15 = line15
        self.line16 = line16
        self.opt_lines = opt_lines
        self.varparent = varparent
        self.spline_terrain_align = spline_terrain_align
        self.rule_list = rule_list

class Rule:
    def __init__(self,
                 kill=False,
                 line1=None,
                 line2=None,
                 line3=None,
                 line4=None
                 ):
        self.kill = kill
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.line4 = line4

class Tile:
    def __init__(self,
                 initial_comment=None,
                 version=None,
                 terrain=False,
                 water=False,
                 variable_terrainlightmap=False,
                 variable_terrain=False,
                 spline=[],
                 _object=[],
                 _files=None
                 ):
        self.initial_comment = initial_comment
        self.version = version
        self.terrain = terrain
        self.water = water
        self.variable_terrainlightmap = variable_terrainlightmap
        self.variable_terrain = variable_terrain
        self.spline = spline
        self._object = _object
        
        self._files = _files
        if self._files is None:
            self._files = omsi_files.OmsiFiles()
    
    def load_files(self, directory, pos_x, pos_y, groundtex_count):
        self._files.add(omsi_files.OmsiFile(map_path=directory,
                                            pattern="tile_{pos_x}_{pos_y}.map.terrain",
                                            params={"pos_x": pos_x, "pos_y": pos_y},
                                            optional=True))
        self._files.add(omsi_files.OmsiFile(map_path=directory,
                                            pattern="tile_{pos_x}_{pos_y}.map.water",
                                            params={"pos_x": pos_x, "pos_y": pos_y},
                                            optional=True))
        self._files.add(omsi_files.OmsiFile(map_path=directory,
                                            pattern="tile_{pos_x}_{pos_y}.map.LM.bmp",
                                            params={"pos_x": pos_x, "pos_y": pos_y},
                                            optional=True))
        self._files.add(omsi_files.OmsiFile(map_path=directory,
                                            pattern="texture/map/tile_{pos_x}_{pos_y}.map.roadmap.bmp",
                                            params={"pos_x": pos_x, "pos_y": pos_y},
                                            optional=True))
        for groundtex_index in range(1, groundtex_count+1):
            self._files.add(omsi_files.OmsiFile(map_path=directory,
                                                pattern="texture/map/tile_{pos_x}_{pos_y}.map.{groundtex_index}.dds",
                                                params={"pos_x": pos_x, "pos_y": pos_y, "groundtex_index": groundtex_index},
                                                optional=True))
    
    def save_files(self, directory):
        self._files.save(directory)
    
    def change_ids(self, value):
        if self.spline is not None:
            for spl in self.spline:
                spl.id = str(int(spl.id) + int(value))
                if spl.id_previous != "0":
                    spl.id_previous = str(int(spl.id_previous) + int(value))
                if spl.id_next != "0":
                    spl.id_next = str(int(spl.id_next) + int(value))
        if self._object is not None:
            for obj in self._object:
                obj.id = str(int(obj.id) + int(value))
                if obj.varparent is not None:
                   obj.varparent = str(int(obj.varparent) + int(value))
    
    def change_groundtex_indexes(self, value):
        for omsi_file in self._files.omsi_files:
            if "groundtex_index" in omsi_file.params:
                omsi_file.params["groundtex_index"] = str(int(omsi_file.params["groundtex_index"])+int(value))
