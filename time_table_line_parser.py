# Copyright 2020 Bartosz Gajewski
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
import time_table_line
import os

class TimeTableLineParser:
    actions = {
        "TIME_TABLE_LINE": [lambda _, n: time_table_line.TimeTableLine(comment1=n[4],
                                                                       comment2=n[5],
                                                                       userallowed=n[7],
                                                                       priority=n[9],
                                                                       tours=n[10])],
        
        "NONEMPTY_LINE": [lambda _, n: n[0]],
        "USERALLOWED_GROUP": [lambda _, n: True],
        "ADDTRIP_GROUP": [lambda _, n: time_table_line.AddTrip(comment=n[0],
                                                               trip_name=n[2],
                                                               line2=n[3],
                                                               depart_time=n[4])],
        "ADDTRIP_GROUP_LIST": [lambda _, n: [n[0]],
                               lambda _, n: n[0] + [n[1]]],
        "NEWTOUR_GROUP": [lambda _, n: time_table_line.NewTour(tour_name=n[3],
                                                               ai_group_name=n[4],
                                                               line3=n[5],
                                                               trips=n[9])],
        "NEWTOUR_GROUP_LIST": [lambda _, n: [n[0]],
                               lambda _, n: n[0] + [n[1]]],
        "OPTIONAL_LINE": [lambda _, n: "",
                          lambda _, n: n[0]],
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "time_table_line_grammar.pg"))
        self.parser = parglare.Parser(self.grammar,
                                      actions=self.actions,
                                      ws="\r")
    def parse(self, file_name):
        with open(file_name, encoding="iso-8859-1") as f:
            content = f.read()
        return self.parser.parse(content)
