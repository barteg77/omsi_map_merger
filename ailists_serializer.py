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

import ailists
import pprint

class AIListsSerializer:
    def serialize(self, ailists_class, file_name):
        with open(file_name, 'w', encoding='utf_16', newline='\r\n') as f:
            self.serialize_(ailists_class, f)
    
    def serialize_(self, ailists_class, f):
        if ailists_class.aigroups is not None:
            for aigroup in ailists_class.aigroups:
                if isinstance(aigroup, ailists.AIGroup2):
                    print("[aigroup_2]", file=f)
                    print(aigroup.name, file=f)
                    print(aigroup.hof_name, file=f)
                    for type in aigroup.types:
                        print(type, file=f)
                    print("[end]", file=f)
                    print(file=f)
                else:
                    print("[aigroup_depot]", file=f)
                    print(aigroup.name, file=f)
                    print(aigroup.hof_name, file=f)
                    print(file=f)
                    for typgroup in aigroup.typgroups:
                        print("[aigroup_depot_typgroup_2]", file=f)
                        print(typgroup.type, file=f)
                        if typgroup.vehicles is not None:
                            for vehicle in typgroup.vehicles:
                                print(vehicle, file=f)
                        print("[end]", file=f)
                        print(file=f)
