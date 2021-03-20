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

class GlobalConfigSerializer:
    def serialize(self, global_config_class, file_name):
        with open(file_name, 'w', encoding='utf16', newline='\r\n') as f:
            self.serialize_(global_config_class, f)

    def serialize_(self, global_config_class, f):
        print(global_config_class.initial_comment, file=f)
        print(file=f)

        print("[name]", file=f)
        print(global_config_class.name, file=f)
        print(file=f)

        print("[friendlyname]", file=f)
        print(global_config_class.friendlyname, file=f)
        print(file=f)

        print("[description]", file=f)
        for line in global_config_class.description:
            print(line, file=f)
        print("[end]", file=f)
        print(file=f)

        print("[version]", file=f)
        print(global_config_class.version, file=f)
        print(file=f)

        print("[NextIDCode]", file=f)
        print(global_config_class.NextIDCode, file=f)
        print(file=f)

        if global_config_class.worldcoordinates:
            print("[worldcoordinates]", file=f)
            print(file=f)

        if global_config_class.dynhelperactive:
            print("[dynhelperactive]", file=f)
            print(file=f)

        if global_config_class.realrail:
            print("[realrail]", file=f)
            print(file=f)

        print("[backgroundimage]", file=f)
        print(global_config_class.backgroundimage.num1, file=f)
        print(global_config_class.backgroundimage.num2, file=f)
        print(global_config_class.backgroundimage.num3, file=f)
        print(global_config_class.backgroundimage.num4, file=f)
        print(global_config_class.backgroundimage.num5, file=f)
        print(global_config_class.backgroundimage.num6, file=f)
        print(file=f)

        print("[mapcam]", file=f)
        print(global_config_class.mapcam.num1, file=f)
        print(global_config_class.mapcam.num2, file=f)
        print(global_config_class.mapcam.num3, file=f)
        print(global_config_class.mapcam.num4, file=f)
        print(global_config_class.mapcam.num5, file=f)
        print(global_config_class.mapcam.num6, file=f)
        print(global_config_class.mapcam.num7, file=f)
        print(global_config_class.mapcam.num8, file=f)
        print(file=f)

        print("[moneysystem]", file=f)
        print(global_config_class.moneysystem, file=f)
        print(file=f)

        print("[ticketpack]", file=f)
        print(global_config_class.ticketpack, file=f)
        print(file=f)

        print("[repair_time_min]", file=f)
        print(global_config_class.repair_time_min, file=f)
        print(file=f)

        if global_config_class.years is not None:
            print("[years]", file=f)
            print(global_config_class.years.num1, file=f)
            print(global_config_class.years.num2, file=f)
            print(file=f)

        if global_config_class.realyearoffset is not None:
            print("[realyearoffset]", file=f)
            print(global_config_class.realyearoffset, file=f)
            #print(file=f)#like OMSI 2 Editor

        print("[standarddepot]", file=f)
        print(global_config_class.standarddepot, file=f)
        print(file=f)

        for gtex in global_config_class.groundtex:
            print("[groundtex]", file=f)
            print(gtex.tex1, file=f)
            print(gtex.tex2, file=f)
            print(gtex.num1, file=f)
            print(gtex.num2, file=f)
            print(gtex.num3, file=f)
            print(file=f)

        for addse in global_config_class.addseason:
            print(addse.description, file=f)
            print("[addseason]", file=f)
            print(addse.num1, file=f)
            print(addse.num2, file=f)
            print(addse.num3, file=f)
            print(file=f)

        for trdero in global_config_class.trafficdensity_road:
            print("[trafficdensity_road]", file=f)
            print(trdero.num1, file=f)
            print(trdero.num2, file=f)
            print(file=f)

        for trdepa in global_config_class.trafficdensity_passenger:
            print("[trafficdensity_passenger]", file=f)
            print(trdepa.num1, file=f)
            print(trdepa.num2, file=f)
            print(file=f)

        print("[entrypoints]", file=f)
        if global_config_class.entrypoints is not None:
            print(len(global_config_class.entrypoints), file=f)
            for enpo in global_config_class.entrypoints:
                print(enpo.object_on_tile_index, file=f)
                print(enpo.id, file=f)
                print(enpo.line3, file=f)
                print(enpo.line4, file=f)
                print(enpo.line5, file=f)
                print(enpo.line6, file=f)
                print(enpo.line7, file=f)
                print(enpo.line8, file=f)
                print(enpo.line9, file=f)
                print(enpo.line10, file=f)
                print(enpo.tile_index, file=f)
                print(enpo.name, file=f)
        else:
            print("0", file=f)
        print(file=f)

        for map_ in global_config_class._map:
            print("[map]", file=f)
            print(map_.pos_x, file=f)
            print(map_.pos_y, file=f)
            print(map_.map_file, file=f)
            print(file=f)
