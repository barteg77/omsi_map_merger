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
import station_links
import os

class StationLinksParser:
    actions={
        "STATION_LINKS": [lambda _, n: station_links.StationLinks(comment1=n[4],
                                                                  comment2=n[5],
                                                                  station_link=n[7]
                                                                  )],
        "NONEMPTY_LINE": [lambda _, n: n[0]],
        "NONEMPTY_LINES": [lambda _, n: [n[0]],
                           lambda _, n: n[0] + [n[1]]],
        "STATION_LINK_ENTRY_GROUP": [lambda _, n: station_links.StationLinkEntry(comment=n[0],
                                                                                 id=n[2],
                                                                                 line2=n[3],
                                                                                 tile_index=n[4],
                                                                                 length=n[5],
                                                                                 line5=n[6],
                                                                                 line6=n[7],
                                                                                 line7=n[8],
                                                                                 chrono_files=n[9]
                                                                                 )],
        "STATION_LINK_ENTRY_GROUP_LIST": [lambda _, n: [n[0]],
                                          lambda _, n: n[0] + [n[1]]],
        "STATION_LINK_GROUP": [lambda _, n: station_links.StationLink(comment=n[0],
                                                                      line1=n[3],
                                                                      id_busstop_start=n[4],
                                                                      id_busstop_end=n[5],
                                                                      line4=n[6],
                                                                      line5=n[7],
                                                                      line6=n[8],
                                                                      line7=n[9],
                                                                      line8=n[10],
                                                                      line9=n[11],
                                                                      station_link_entry=n[13]
                                                                      )],
        "STATION_LINK_GROUP_LIST": [lambda _, n: [n[0]],
                                    lambda _, n: n[0] + [n[1]]]
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "station_links_grammar.pg"))
        self.parser = parglare.GLRParser(self.grammar,
                                         actions=self.actions,
                                         ws="\r")
    def parse(self, file_name):
        with open(file_name, encoding="iso-8859-1") as f:
            content = f.read()
        return self.parser.parse(content)[0]
