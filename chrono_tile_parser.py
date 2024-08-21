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

import parglare
import chrono_tile
import tile
import os

class ChronoTileParser():
    actions = {
        "CHRONO_TILE": [lambda _, n: chrono_tile.ChronoTile(initial_comment=n[0],
                                                            version=n[2],
                                                            elements_list=n[3] if n[3] is not None else [],
                                                            )],
        "VERSION_GROUP": [lambda _, n: n[1]],
        "SELECT_GROUP_HEADER": [lambda _, n: True,
                                lambda _, n: False],
        "SELECT_GROUP": [lambda _, n: chrono_tile.Select(spline=n[0],
                                                         id=int(n[1]),
                                                         lines=n[2] if n[2] is not None else []
                                                         )],
        "SPLINE_TERRAIN_ALIGN_2_GROUP": [lambda _, n: n[1]],
        "MIRROR_GROUP": [lambda _, n: True,
                         lambda _, n: False],
        "SPLINE_GROUP": [lambda _, n: tile.Spline(h=False,
                                                  line1=n[1],
                                                  file_name=n[2],
                                                  id=n[3],
                                                  id_previous=n[4],
                                                  id_next=n[5],
                                                  pos_x=n[6],
                                                  pos_z=n[7],
                                                  pos_y=n[8],
                                                  rotate=n[9],
                                                  length=n[10],
                                                  radius=n[11],
                                                  gradient_start=n[12],
                                                  gradient_end=n[13],
                                                  delta_h=None,
                                                  cant_start=n[14],
                                                  cant_end=n[15],
                                                  skew_start=n[16],
                                                  skew_end=n[17],
                                                  line18=n[18],
                                                  mirror=n[19],
                                                  spline_terrain_align_2=n[21],
                                                  rule_list=n[22]
                                                  )],
        "SPLINE_H_GROUP": [lambda _, n: tile.Spline(h=True,
                                                    line1=n[1],
                                                    file_name=n[2],
                                                    id=n[3],
                                                    id_previous=n[4],
                                                    id_next=n[5],
                                                    pos_x=n[6],
                                                    pos_z=n[7],
                                                    pos_y=n[8],
                                                    rotate=n[9],
                                                    length=n[10],
                                                    radius=n[11],
                                                    gradient_start=n[12],
                                                    gradient_end=n[13],
                                                    delta_h = n[14],
                                                    cant_start=n[15],
                                                    cant_end=n[16],
                                                    skew_start=n[17],
                                                    skew_end=n[18],
                                                    line18=n[19],
                                                    mirror=n[20],
                                                    spline_terrain_align_2=n[22],
                                                    rule_list=n[23]
                                                    )],
        "LINES": [lambda _, n: [n[0]],
                  lambda _, n: n[0] + [n[1]]],
        "SPLINE_TERRAIN_ALGIN_GROUP": [lambda _, n: True],
        "OBJECT_HEADER_GROUP": [lambda _, n: False,
                                lambda _, n: True],
        "OBJECT_GROUP": [lambda _, n: tile._Object(description=n[0],
                                                   attach_object=n[1],
                                                   line1=n[2],
                                                   file_name=n[3],
                                                   id=n[4],
                                                   pos_x=n[5],
                                                   pos_y=n[6],
                                                   pos_z=n[7],
                                                   rotate=n[8],
                                                   pitch=n[9],
                                                   bank=n[10],
                                                   line10=n[11],
												   opt_lines=n[12],
                                                   varparent=n[14],
                                                   spline_terrain_align=n[15],
                                                   rule_list=n[16]
                                                   )],
        "SPLINEATTACHEMENT_GROUP": [lambda _, n: tile.SplineAttachement(description=n[0],
                                                                        line1=n[2],
                                                                        file_name=n[3],
                                                                        id=n[4],
                                                                        line4=n[5],
                                                                        pos_x=n[6],
                                                                        pos_z=n[7],
                                                                        pos_y=n[8],
                                                                        rotate=n[9],
                                                                        pitch=n[10],
                                                                        bank=n[11],
                                                                        interval=n[12],
                                                                        distance=n[13],
                                                                        line13=n[14],
                                                                        line14=n[15],
                                                                        opt_lines=n[16],
                                                                        varparent=n[18],
                                                                        spline_terrain_align=n[19],
                                                                        rule_list=n[20]
                                                                        )],
        "SPLINEATTACHEMENT_REPEATER_GROUP": [lambda _, n: tile.SplineAttachementRepeater(description=n[0],
                                                                                         line1=n[2],
                                                                                         line2=n[3],
                                                                                         line3=n[4],
                                                                                         file_name=n[5],
                                                                                         id=n[6],
                                                                                         line6=n[7],
                                                                                         pos_x=n[8],
                                                                                         pos_z=n[9],
                                                                                         pos_y=n[10],
                                                                                         rotate=n[11],
                                                                                         pitch=n[12],
                                                                                         bank=n[13],
                                                                                         interval=n[14],
                                                                                         distance=n[15],
                                                                                         line15=n[16],
                                                                                         line16=n[17],
                                                                                         opt_lines=n[18],
                                                                                         varparent=n[20],
                                                                                         spline_terrain_align=n[21],
                                                                                         rule_list=n[22]
                                                                                         )],
        "VARPARENT_GROUP": [lambda _, n: n[1]],
        "RULE_GROUP": [lambda _, n: tile.Rule(kill=False,
                                              line1=n[1],
                                              line2=n[2],
                                              line3=n[3],
                                              line4=n[4]
                                              )],
        "KILL_RULE_GROUP": [lambda _, n: tile.Rule(kill=True,
                                                   line1=n[1],
                                                   line2=n[2],
                                                   line3=n[3],
                                                   line4=n[4]
                                                   )],
        "RULE_GROUP_LIST": [lambda _, n: [n[0]],
                            lambda _, n: [n[0]],
                            lambda _, n: n[0] + [n[1]],
                            lambda _, n: n[0] + [n[1]]],
        "OPTIONAL_LINE": [lambda _, n: "",
                          lambda _, n: n[0]],
        
        "GROUP_LIST": [lambda _, n: [n[0]],
                       lambda _, n: [n[0]],
                       lambda _, n: [n[0]],
                       lambda _, n: [n[0]],
                       lambda _, n: [n[0]],
                       lambda _, n: [n[0]],
                       lambda _, n: n[0] + [n[1]],
                       lambda _, n: n[0] + [n[1]],
                       lambda _, n: n[0] + [n[1]],
                       lambda _, n: n[0] + [n[1]],
                       lambda _, n: n[0] + [n[1]],
                       lambda _, n: n[0] + [n[1]]],
        
		"NONEMPTY_LINE": [lambda _, n: n[0]]
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chrono_tile_grammar.pg"))
        self.parser = parglare.GLRParser(self.grammar,
                                         actions=self.actions,
                                         ws="\r")
    def parse(self, file_name):
        with open(file_name, encoding="utf16") as f:
            content = f.read()
        return self.parser.parse(content)[0]
