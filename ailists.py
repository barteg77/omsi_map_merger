# Copyright 2020, 2021 Bartosz Gajewski
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

class AIGroup2:
    def __init__(self,
                 name,
                 hof_name=None,
                 types=None
                 ):
        self.name = name
        self.hof_name = hof_name
        self.types = types

class AIGroupDepotTypgroup2:
    def __init__(self,
                 type,
                 vehicles
                 ):
        self.type = type
        self.vehicles = vehicles

class AIGroupDepot:
    def __init__(self,
                 name,
                 hof_name,
                 typgroups):
        self.name = name
        self.hof_name = hof_name
        self.typgroups = typgroups

class AILists:
    def __init__(self,
                 aigroups=None
                 ):
        self.aigroups = aigroups
