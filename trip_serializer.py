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

import trip

class TripSerializer:
    def serialize(self, trip_object, file_name):
        with open(file_name, 'w', encoding='iso-8859-1', newline='\r\n') as f:
            self.serialize_(trip_object, f)
    
    def serialize_(self, trip_object: trip.Trip, f):
        print("-----------------------", file=f)
        print("Time Table Trip File", file=f)
        print("-----------------------", file=f)
        print(file=f)
        print(trip_object.comment1, file=f)
        print(trip_object.comment2, file=f)
        print(file=f)
        print("[trip]", file=f)
        print(trip_object.line1, file=f)
        print(trip_object.line2, file=f)
        print(trip_object.line3, file=f)
        print(file=f)
        print(".........................", file=f)
        print("        Stations", file=f)
        print(".........................", file=f)
        print(file=f)
        for station in trip_object.station:
            if type(station) == trip.StationTyp2:
                print("[station_typ2]", file=f)
                print(station.id, file=f)
                print(file=f)
            elif type(station) == trip.Station:
                print("[station]", file=f)
                print(station.id, file=f)
                print(station.interval, file=f)
                print(station.name, file=f)
                print(station.tile_index, file=f)
                print(station.line5, file=f)
                print(station.line6, file=f)
                print(station.line7, file=f)
                print(station.line8, file=f)
                print(file=f)
            else:
                assert False, f"station of not allowed type: {type(station)}"
        print(file=f)
        print(".........................", file=f)
        print("        Profiles", file=f)
        print(".........................", file=f)
        print(file=f)
        if trip_object.lines is not None:
            for line in trip_object.lines:
                print(line, file=f)
