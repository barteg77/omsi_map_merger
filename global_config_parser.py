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
import global_config
import os

class GlobalConfigParser():
    actions = {
        "GLOBAL_CONFIG": [lambda _, n: global_config.GlobalConfig(initial_comment=n[0],
                                                                  name=n[1],
                                                                  friendlyname=n[2],
                                                                  description=n[3],
                                                                  version=n[4],
                                                                  NextIDCode=int(n[5]),
                                                                  worldcoordinates=n[6],
                                                                  dynhelperactive=n[7],
                                                                  realrail=n[8],
                                                                  backgroundimage=n[9],
                                                                  mapcam=n[10],
                                                                  moneysystem=n[11],
                                                                  ticketpack=n[12],
                                                                  repair_time_min=n[13],
                                                                  years=n[14],
                                                                  realyearoffset=n[15],
                                                                  standarddepot=n[16],
                                                                  groundtex=n[17],
                                                                  addseason=n[18],
                                                                  trafficdensity_road=n[19],
                                                                  trafficdensity_passenger=n[20],
                                                                  entrypoints=n[21],
                                                                  _map=n[22]
                                                                  )],
        "INITIAL_COMMENT_GROUP": [lambda _, n: n[0]],
        "NAME_GROUP": [lambda _, n: n[1]],
        "FRIENDLYNAME_GROUP": [lambda _, n: n[1]],
        "DESCRIPTION_GROUP": [lambda _, n: n[1]],
        "LINES": [lambda _, n: [n[0]],
                  lambda _, n: n[0] + [n[1]]],
        "DESCRIPTION_LINE": [lambda _, n: "",
                             lambda _, n: n[0]],
        "VERSION_GROUP": [lambda _, n: n[1]],
        "NEXTIDCODE_GROUP": [lambda _, n: n[1]],
        "WORLDCOORDINATES_GROUP": [lambda _, n: True],
        "DYNHELPERACTIVE_GROUP": [lambda _, n: True],
        "REALRAIL_GROUP": [lambda _, n: True],
        "BACKGROUNDIMAGE_GROUP": [lambda _, n: global_config.BackgroundImage(num1=n[1],
                                                                             num2=n[2],
                                                                             num3=n[3],
                                                                             num4=n[4],
                                                                             num5=n[5],
                                                                             num6=n[6]
                                                                             )],
        "MAPCAM_GROUP": [lambda _, n: global_config.MapCam(num1=n[1],
                                                           num2=n[2],
                                                           num3=n[3],
                                                           num4=n[4],
                                                           num5=n[5],
                                                           num6=n[6],
                                                           num7=n[7],
                                                           num8=n[8]
                                                           )],
        "MONEYSYSTEM_GROUP": [lambda _, n: n[1]],
        "TICKETPACK_GROUP": [lambda _, n: n[1]],
        "REPAIR_TIME_MIN_GROUP": [lambda _, n: n[1]],
        "YEARS_GROUP": [lambda _, n: global_config.Years(num1=n[1],
                                                         num2=n[2]
                                                         )],
        "REALYEAROFFSET_GROUP": [lambda _, n: n[1]],
        "STANDARDDEPOT_GROUP": [lambda _, n: n[1]],
        "GROUNDTEX_GROUP": [lambda _, n: global_config.GroundTex(tex1=n[1],
                                                                 tex2=n[2],
                                                                 num1=n[3],
                                                                 num2=n[4],
                                                                 num3=n[5]
                                                                 )],
        "GROUNDTEX_GROUP_LIST": [lambda _, n: [n[0]],
                                 lambda _, n: n[0] + [n[1]]],
        "ADDSEASON_GROUP": [lambda _, n: global_config.AddSeason(description=n[0],
                                                                 num1=n[2],
                                                                 num2=n[3],
                                                                 num3=n[4]
                                                                 )],
        "ADDSEASON_GROUP_LIST": [lambda _, n: [n[0]],
                                 lambda _, n: n[0] + [n[1]]],
        "TRAFFICDENSITY_ROAD_GROUP": [lambda _, n: global_config.Trafficdensity(num1=n[1],
                                                                                num2=n[2]
                                                                                )],
        "TRAFFICDENSITY_ROAD_GROUP_LIST": [lambda _, n: [n[0]],
                                           lambda _, n: n[0] + [n[1]]],
        "TRAFFICDENSITY_PASSENGER_GROUP": [lambda _, n: global_config.Trafficdensity(num1=n[1],
                                                                                     num2=n[2]
                                                                                     )],
        "TRAFFICDENSITY_PASSENGER_GROUP_LIST": [lambda _, n: [n[0]],
                                                lambda _, n: n[0] + [n[1]]],
        "ENTRYPOINTS_GROUP": [lambda _, n: global_config.Entrypoints(object_on_tile_index=n[0],
                                                                     id=int(n[1]),
                                                                     line3=n[2],
                                                                     line4=n[3],
                                                                     line5=n[4],
                                                                     line6=n[5],
                                                                     line7=n[6],
                                                                     line8=n[7],
                                                                     line9=n[8],
                                                                     line10=n[9],
                                                                     tile_index=int(n[10]),
                                                                     name=n[11],
                                                                     )],
        "ENTRYPOINTS_GROUP_LIST_": [lambda _, n: [n[0]],
                                    lambda _, n: n[0] + [n[1]]],
        "ENTRYPOINTS_GROUP_LIST": [lambda _, n:n[2]],
        "MAP_GROUP": [lambda _, n: global_config.Map(pos_x=int(n[1]),
                                                     pos_y=int(n[2]),
                                                     map_file=n[3]
                                                     )],
        "MAP_GROUP_LIST": [lambda _, n: [n[0]],
                           lambda _, n: n[0] + [n[1]]],
        "OPTIONAL_LINE": [lambda _, n: "",
                          lambda _, n: n[0]],
        "OPTIONAL_STRANGE_LINE": [lambda _, n: "",
                                  lambda _, n: n[0],
                                  lambda _, n: n[0]],
        "NONEMPTY_LINE": [lambda _, n: n[0]],
        "ADDSEASON_LINE": [lambda _, n: n[0]]
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "global_config_grammar.pg"))
        self.parser = parglare.Parser(self.grammar,
                                      actions=self.actions,
                                      ws="\r")

    def parse(self, file_name):
        with open(file_name, encoding="utf_16_le") as f:
            content = f.read()
        return self.parser.parse(content)
