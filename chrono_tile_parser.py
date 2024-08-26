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
import tile_parser
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
        "SPLINE_GROUP": tile_parser.TileParser.actions["SPLINE_GROUP"],
        "SPLINE_H_GROUP": tile_parser.TileParser.actions["SPLINE_H_GROUP"],
        "LINES": [lambda _, n: [n[0]],
                  lambda _, n: n[0] + [n[1]]],
        "SPLINE_TERRAIN_ALGIN_GROUP": [lambda _, n: True],
        "OBJECT_HEADER_GROUP": [lambda _, n: False,
                                lambda _, n: True],
        "OBJECT_GROUP": tile_parser.TileParser.actions["OBJECT_GROUP"],
        "SPLINEATTACHEMENT_GROUP": tile_parser.TileParser.actions["SPLINEATTACHEMENT_GROUP"],
        "SPLINEATTACHEMENT_REPEATER_GROUP": tile_parser.TileParser.actions["SPLINEATTACHEMENT_REPEATER_GROUP"],
        "VARPARENT_GROUP": [lambda _, n: n[1]],
        "RULE_GROUP": tile_parser.TileParser.actions["RULE_GROUP"],
        "KILL_RULE_GROUP": tile_parser.TileParser.actions["KILL_RULE_GROUP"],
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
        with open(file_name, encoding="utf_16_le") as f:
            content = f.read()
        return self.parser.parse(content)[0]
