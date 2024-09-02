# Copyright 2020, 2024 Bartosz Gajewski
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

import tile
class TileSerializer:
    def serialize(self, tile_class, file_name):
        with open(file_name, 'w', encoding='utf_16', newline='\r\n') as f:
            self.serialize_(tile_class, f)

    def serialize_(self, tile_class, f):
        print(tile_class.initial_comment, file=f)
        print(file=f)

        print("[version]", file=f)
        print(tile_class.version, file=f)
        print(file=f)

        if tile_class.terrain:
            print("[terrain]", file=f)
            print(file=f)
            print(file=f)#like OMSI 2 Editor
        
        if tile_class.water:
            print("[water]", file=f)
            print(file=f)
            print(file=f)

        if tile_class.variable_terrainlightmap:
            print("[variable_terrainlightmap]", file=f)
            print(file=f)

        if tile_class.variable_terrain:
            print("[variable_terrain]", file=f)
            print(file=f)
        
        if tile_class.spline is not None:
            for spl in tile_class.spline:
                if spl.h:
                    print("[spline_h]", file=f)
                else:
                    print("[spline]", file=f)
                print(spl.line1, file=f)
                print(spl.file_name, file=f)
                print(spl.id, file=f)
                print(spl.id_previous, file=f)
                print(spl.id_next, file=f)
                print(spl.pos_x, file=f)
                print(spl.pos_z, file=f)
                print(spl.pos_y, file=f)
                print(spl.rotate, file=f)
                print(spl.length, file=f)
                print(spl.radius, file=f)
                print(spl.gradient_start, file=f)
                print(spl.gradient_end, file=f)
                if spl.h:
                    print(spl.delta_h, file=f)
                print(spl.cant_start, file=f)
                print(spl.cant_end, file=f)
                print(spl.skew_start, file=f)
                print(spl.skew_end, file=f)
                print(spl.line18, file=f)
                if spl.mirror:
                    print("mirror", file=f)
                else:
                    print(file=f)
                if spl.spline_terrain_align_2 != "" and spl.spline_terrain_align_2 is not None:
                    print(file=f)
                    print("[spline_terrain_align_2]", file=f)
                    print(spl.spline_terrain_align_2, file=f)
                if spl.rule_list is not None:
                    for rul in spl.rule_list:
                        print(file=f)
                        if rul.kill:
                            print("[kill_rule]", file=f)
                        else:
                            print("[rule]", file=f)
                        print(rul.line1, file=f)
                        print(rul.line2, file=f)
                        print(rul.line3, file=f)
                        print(rul.line4, file=f)
                print(file=f)
        
        if tile_class._object is not None:
            for obj in tile_class._object:
                print(obj.description, file=f)
                if isinstance(obj, tile._Object):
                    if obj.attach_object:
                        print("[attachObj]", file=f)
                    else:
                        print("[object]", file=f)
                    print(obj.line1, file=f)
                    print(obj.file_name, file=f)
                    print(obj.id, file=f)
                    print(obj.pos_x, file=f)
                    print(obj.pos_y, file=f)
                    print(obj.pos_z, file=f)
                    print(obj.rotate, file=f)
                    print(obj.pitch, file=f)
                    print(obj.bank, file=f)
                    print(obj.line10, file=f)
                elif isinstance(obj, tile.SplineAttachement):
                    print("[splineAttachement]", file=f)
                    print(obj.line1, file=f)
                    print(obj.file_name, file=f)
                    print(obj.id, file=f)
                    print(obj.line4, file=f)
                    print(obj.pos_x, file=f)
                    print(obj.pos_z, file=f)
                    print(obj.pos_y, file=f)
                    print(obj.rotate, file=f)
                    print(obj.pitch, file=f)
                    print(obj.bank, file=f)
                    print(obj.interval, file=f)
                    print(obj.distance, file=f)
                    print(obj.line13, file=f)
                    print(obj.line14, file=f)
                elif isinstance(obj, tile.SplineAttachementRepeater):
                    print("[splineAttachement_repeater]", file=f)
                    print(obj.line1, file=f)
                    print(obj.line2, file=f)
                    print(obj.line3, file=f)
                    print(obj.file_name, file=f)
                    print(obj.id, file=f)
                    print(obj.line6, file=f)
                    print(obj.pos_x, file=f)
                    print(obj.pos_z, file=f)
                    print(obj.pos_y, file=f)
                    print(obj.rotate, file=f)
                    print(obj.pitch, file=f)
                    print(obj.bank, file=f)
                    print(obj.interval, file=f)
                    print(obj.distance, file=f)
                    print(obj.line15, file=f)
                    print(obj.line16, file=f)
                if obj.opt_lines is not None:
                    for ol in obj.opt_lines:
                        print(ol, file=f)
                print(file=f)
                if obj.varparent is not None:
                    print("[varparent]", file=f)
                    print(obj.varparent, file=f)
                    print(file=f)
                if obj.spline_terrain_align:
                    print("[spline_terrain_align]", file=f)
                    print(file=f)
                if obj.rule_list is not None:
                    for rul in obj.rule_list:
                        if rul.kill:
                            print("[kill_rule]", file=f)
                        else:
                            print("[rule]", file=f)
                        print(rul.line1, file=f)
                        print(rul.line2, file=f)
                        print(rul.line3, file=f)
                        print(rul.line4, file=f)
                        print(file=f)
