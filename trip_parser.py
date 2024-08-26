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
import trip
import os

class TripParser:
    actions = {
        "TRIP": [lambda _, n: trip.Trip(comment1=n[4],
                                        comment2=n[5],
                                        line1=n[8],
                                        line2=n[9],
                                        line3=n[10],
                                        station=n[16] if n[16] is not None else [],
                                        lines=n[22]
                                        )],
        "NONEMPTY_LINE": [lambda _, n: n[0]],
        "STATION_TYP2_GROUP": [lambda _, n: trip.StationTyp2(int(n[1]))],
        "STATION_TYP2_GROUP_LIST": [lambda _, n: [n[0]],
                                    lambda _, n: n[0] + [n[1]]],
        "STATION_GROUP": [lambda _, n: trip.Station(id=int(n[1]),
                                                    interval=n[2],
                                                    name=n[3],
                                                    tile_index=int(n[4]),
                                                    line5=n[5],
                                                    line6=n[6],
                                                    line7=n[7],
                                                    line8=n[8]
                                                    )],
        "STATION_GROUP_LIST": [lambda _, n: [n[0]],
                               lambda _, n: n[0] + [n[1]]],
        "STATIONS": [lambda _, n: n[0],
                     lambda _, n: n[0]],
        "OPTIONAL_LINE": [lambda _, n: "",
                          lambda _, n: n[0]],
        "LINES": [lambda _, n: [n[0]],
                  lambda _, n: n[0] + [n[1]]],
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "trip_grammar.pg"))
        self.parser = parglare.Parser(self.grammar,
                                      actions=self.actions,
                                      ws="\r")
    def parse(self, file_name):
        with open(file_name, encoding="iso-8859-1") as f:
            content = f.read()
        return self.parser.parse(content)
