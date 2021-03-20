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
import track
import os

class TrackParser():
    actions = {
        "TRACK": [lambda _, n: track.Track(comment1=n[4],
                                           comment2=n[5],
                                           track_entry=n[7]
                                           )],
        "NONEMPTY_LINE": [lambda _, n: n[0]],
        "TRACK_ENTRY_GROUP": [lambda _, n: track.TrackEntry(comment=n[0],
                                                            id=n[2],
                                                            line2=n[3],
                                                            tile_index=n[4],
                                                            line4=n[5],
                                                            length=n[6],
                                                            line6=n[7],
                                                            line7=n[8],
                                                            )],
        "TRACK_ENTRY_GROUP_LIST": [lambda _, n: [n[0]],
                                   lambda _, n: n[0] + [n[1]]]
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "track_grammar.pg"))
        self.parser = parglare.Parser(self.grammar,
                                      actions=self.actions,
                                      ws="\r")
    def parse(self, file_name):
        with open(file_name, encoding="iso-8859-1") as f:
            content = f.read()
        return self.parser.parse(content)
