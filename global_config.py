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

class BackgroundImage:
    def __init__(self,
                 num1="",
                 num2="",
                 num3="",
                 num4="",
                 num5="",
                 num6="",
                 ):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.num4 = num4
        self.num5 = num5
        self.num6 = num6

class MapCam:
    def __init__(self,
                 num1="",
                 num2="",
                 num3="",
                 num4="",
                 num5="",
                 num6="",
                 num7="",
                 num8=""
                 ):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.num4 = num4
        self.num5 = num5
        self.num6 = num6
        self.num7 = num7
        self.num8 = num8

class Years:
    def __init__(self,
                 num1="",
                 num2=""
                 ):
        self.num1 = num1
        self.num2 = num2

class GroundTex:
    def __init__(self,
                 tex1="",
                 tex2="",
                 num1="",
                 num2="",
                 num3=""):
        self.tex1 = tex1
        self.tex2 = tex2
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3

class AddSeason:
    def __init__(self,
                 description="",
                 num1="",
                 num2="",
                 num3=""
                 ):
        self.description = description
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3

class Trafficdensity:
    def __init__(self,
                 num1=0,
                 num2=0
                 ):
        self.num1 = num1
        self.num2 = num2

class Entrypoints:
    def __init__(self,
                 object_on_tile_index=None,
                 id=None,
                 line3=None,
                 line4=None,
                 line5=None,
                 line6=None,
                 line7=None,
                 line8=None,
                 line9=None,
                 line10=None,
                 tile_index=None,
                 name=None
                 ):
        self.object_on_tile_index = object_on_tile_index
        self.id = id
        self.line3 = line3
        self.line4 = line4
        self.line5 = line5
        self.line6 = line6
        self.line7 = line7
        self.line8 = line8
        self.line9 = line9
        self.line10 = line10
        self.tile_index = tile_index
        self.name = name

class Map:
    def __init__(self,
                 pos_x=0,
                 pos_y=0,
                 map_file=""
                 ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.map_file = map_file

class GlobalConfig:
    def __init__(self,
                 initial_comment="",
                 name="",
                 friendlyname="",
                 description=[],
                 version="",
                 NextIDCode=0,
                 worldcoordinates=False,
                 dynhelperactive=False,
                 realrail=False,
                 backgroundimage=BackgroundImage(),
                 mapcam=MapCam(),
                 moneysystem="",
                 ticketpack="",
                 repair_time_min="",
                 years=Years(),
                 realyearoffset="",
                 standarddepot="",
                 groundtex=[],
                 addseason=[],
                 trafficdensity_road=[],
                 trafficdensity_passenger=[],
                 entrypoints=[],
                 _map=[]
                 ):
        self.initial_comment = initial_comment
        self.name = name
        self.friendlyname = friendlyname
        self.description = description
        self.version = version
        self.NextIDCode = NextIDCode
        self.worldcoordinates = worldcoordinates
        self.dynhelperactive = dynhelperactive
        self.realrail = realrail
        self.backgroundimage = backgroundimage
        self.mapcam = mapcam
        self.moneysystem = moneysystem
        self.ticketpack = ticketpack
        self.repair_time_min = repair_time_min
        self.years = years
        self.realyearoffset = realyearoffset
        self.standarddepot = standarddepot
        self.groundtex = groundtex
        self.addseason = addseason
        self.trafficdensity_road = trafficdensity_road
        self.trafficdensity_passenger = trafficdensity_passenger
        self.entrypoints = entrypoints
        self._map = _map
        
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        for entrypoint in self.entrypoints:
            entrypoint.id = str(int(entrypoint.id) + int(ids_value))
            entrypoint.tile_index = str(int(entrypoint.tile_index) + int(tile_indexes_value))
