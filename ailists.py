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

class AnyAIgroup:
    def __init__(self) -> None:
        self.name: str
        self.type: str
        raise NotImplementedError("this is abstract class")
    
    def __key(self):
        return (self.name, self.type)
    
    def __eq__(self, other: 'AnyAIgroup') -> bool:
        return self.__key() == other.__key()

class AIGroup2(AnyAIgroup):
    def __init__(self,
                 name,
                 hof_name=None,
                 types=None
                 ):
        self.name = name
        self.hof_name = hof_name
        self.types = types
    
    def __key(self):
        return (self.name, self.hof_name, self.types)
    
    def __eq__(self, other: 'AIGroup2') -> bool:
        return self.__key() == other.__key()

class AIGroupDepotTypgroup2:
    def __init__(self,
                 type,
                 vehicles
                 ):
        self.type = type
        self.vehicles = vehicles
    
    def __key(self):
        return (self.type, self.vehicles)
    
    def __eq__(self, other: 'AIGroupDepotTypgroup2') -> bool:
        return self.__key() == other.__key()

class AIGroupDepot(AnyAIgroup):
    def __init__(self,
                 name: str,
                 hof_name: str,
                 typgroups: list[AIGroupDepotTypgroup2]):
        self.name: str = name
        self.hof_name: str = hof_name
        self.typgroups: list[AIGroupDepotTypgroup2] = typgroups
    
    def __key(self):
        return (self.name, self.hof_name, self.typgroups)
    
    def __eq__(self, other: 'AIGroupDepot') -> bool:
        return self.__key() == other.__key()

class AILists:
    def __init__(self,
                 aigroups: list[AnyAIgroup],
                 ):
        self.aigroups: list[AnyAIgroup] = aigroups
    
    def __key(self):
        return (self.aigroups)
    
    def __eq__(self, other: 'AILists') -> bool:
        return self.__key() == other.__key()