# Copyright 2020, 2021, 2024 Bartosz Gajewski
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
import charset_normalizer
import ailists
import os
import logging

logger = logging.getLogger(__name__)

class AIListsParser():
    actions = {
        "AILISTS": [lambda _, n: ailists.AILists(aigroups=n[1])],
        "AIGROUP_2_GROUP": [lambda _, n: ailists.AIGroup2(name=n[1],
                                                          hof_name=n[2],
                                                          types=n[3])],
        "AIGROUP_DEPOT_TYPGROUP_2_GROUP": [lambda _, n: ailists.AIGroupDepotTypgroup2(type=n[1],
                                                                                      vehicles=n[2])],
        "AIGROUP_DEPOT_TYPGROUP_2_GROUP_LIST": [lambda _, n: [n[0]],
                                                lambda _, n: n[0] + [n[1]]],
        "AIGROUP_DEPOT_GROUP": [lambda _, n: ailists.AIGroupDepot(name=n[1],
                                                                  hof_name=n[2],
                                                                  typgroups=n[4])],
        "AIGROUP_GROUP": [lambda _, n: n[0],
                          lambda _, n: n[0]],
        "AIGROUP_GROUP_LIST": [lambda _, n: [n[0]],
                               lambda _, n: n[0] + [n[1]]],
        "OPTIONAL_LINE": [lambda _, n: "",
                          lambda _, n: n[0]],
		"LINES": [lambda _, n: [n[0]],
                  lambda _, n: n[0] + [n[1]]],
        "DESCRIPTION_LINE": [lambda _, n: "",
                             lambda _, n: n[0]],
    }
    def __init__(self):
        self.grammar = parglare.Grammar.from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ailists_grammar.pg"))
        self.parser = parglare.GLRParser(self.grammar,
                                         actions=self.actions,
                                         ws="\r")
    def parse(self, file_name):
        best_match = charset_normalizer.from_path(file_name).best()
        content: str = '\n'.join(str(best_match).splitlines())
        logger.debug(f"Decoded ailists: {repr(content)}")
        return self.parser.parse(content)[0]
