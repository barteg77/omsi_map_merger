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

import chrono_tile
import tile

class ChronoTileSerializer:
    def serialize(self, tile_class, file_name):
        with open(file_name, 'w', encoding='utf_16', newline='\r\n') as f:
            self.serialize_(tile_class, f)

    def serialize_(self, chrono_tile_obj: chrono_tile.ChronoTile, f):
        print(chrono_tile_obj.initial_comment, file=f)
        print(file=f)

        print("[version]", file=f)
        print(chrono_tile_obj.version, file=f)
        print(file=f)
    
        for entry in chrono_tile_obj.elements_list:
            if isinstance(entry, chrono_tile.Select):
                if entry.spline:
                    print("[selspline]", file=f)
                else:
                    print("[selobject]", file=f)
                print(entry.id, file=f)
                for line in entry.lines:
                    print(line, file=f)

            elif isinstance(entry, tile.Spline):
                if entry.h:
                    print("[spline_h]", file=f)
                else:
                    print("[spline]", file=f)
                print(entry.line1, file=f)
                print(entry.file_name, file=f)
                print(entry.id, file=f)
                print(entry.id_previous, file=f)
                print(entry.id_next, file=f)
                print(entry.pos_x, file=f)
                print(entry.pos_z, file=f)
                print(entry.pos_y, file=f)
                print(entry.rotate, file=f)
                print(entry.length, file=f)
                print(entry.radius, file=f)
                print(entry.gradient_start, file=f)
                print(entry.gradient_end, file=f)
                if entry.h:
                    print(entry.delta_h, file=f)
                print(entry.cant_start, file=f)
                print(entry.cant_end, file=f)
                print(entry.skew_start, file=f)
                print(entry.skew_end, file=f)
                print(entry.line18, file=f)
                if entry.mirror:
                    print("mirror", file=f)
                else:
                    print(file=f)
                if entry.spline_terrain_align_2 != "" and entry.spline_terrain_align_2 is not None:
                    print(file=f)
                    print("[spline_terrain_align_2]", file=f)
                    print(entry.spline_terrain_align_2, file=f)
                if entry.rule_list is not None:
                    for rul in entry.rule_list:
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
    
            elif isinstance(entry, tile._Object) or isinstance(entry, tile.SplineAttachement) or isinstance(entry, tile.SplineAttachementRepeater):
                print(entry.description, file=f)
                if isinstance(entry, tile._Object):
                    if entry.attach_object:
                        print("[attachObj]", file=f)
                    else:
                        print("[object]", file=f)
                    print(entry.line1, file=f)
                    print(entry.file_name, file=f)
                    print(entry.id, file=f)
                    print(entry.pos_x, file=f)
                    print(entry.pos_y, file=f)
                    print(entry.pos_z, file=f)
                    print(entry.rotate, file=f)
                    print(entry.pitch, file=f)
                    print(entry.bank, file=f)
                    print(entry.line10, file=f)
                elif isinstance(entry, tile.SplineAttachement):
                    print("[splineAttachement]", file=f)
                    print(entry.line1, file=f)
                    print(entry.file_name, file=f)
                    print(entry.id, file=f)
                    print(entry.line4, file=f)
                    print(entry.pos_x, file=f)
                    print(entry.pos_z, file=f)
                    print(entry.pos_y, file=f)
                    print(entry.rotate, file=f)
                    print(entry.pitch, file=f)
                    print(entry.bank, file=f)
                    print(entry.interval, file=f)
                    print(entry.distance, file=f)
                    print(entry.line13, file=f)
                    print(entry.line14, file=f)
                elif isinstance(entry, tile.SplineAttachementRepeater):
                    print("[splineAttachement_repeater]", file=f)
                    print(entry.line1, file=f)
                    print(entry.line2, file=f)
                    print(entry.line3, file=f)
                    print(entry.file_name, file=f)
                    print(entry.id, file=f)
                    print(entry.line6, file=f)
                    print(entry.pos_x, file=f)
                    print(entry.pos_z, file=f)
                    print(entry.pos_y, file=f)
                    print(entry.rotate, file=f)
                    print(entry.pitch, file=f)
                    print(entry.bank, file=f)
                    print(entry.interval, file=f)
                    print(entry.distance, file=f)
                    print(entry.line15, file=f)
                    print(entry.line16, file=f)
                if entry.opt_lines is not None:
                    for ol in entry.opt_lines:
                        print(ol, file=f)
                print(file=f)
                if entry.varparent is not None:
                    print("[varparent]", file=f)
                    print(entry.varparent, file=f)
                    print(file=f)
                if entry.spline_terrain_align:
                    print("[spline_terrain_align]", file=f)
                    print(file=f)
                if entry.rule_list is not None:
                    for rul in entry.rule_list:
                        if rul.kill:
                            print("[kill_rule]", file=f)
                        else:
                            print("[rule]", file=f)
                        print(rul.line1, file=f)
                        print(rul.line2, file=f)
                        print(rul.line3, file=f)
                        print(rul.line4, file=f)
                        print(file=f)
