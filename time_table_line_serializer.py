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

import time_table_line

class TimeTableLineSerializer:
    def serialize(self, time_table_line_class, file_name):
        with open(file_name, 'w', encoding='iso-8859-1', newline='\r\n') as f:
            self.serialize_(time_table_line_class, f)
    
    def serialize_(self, time_table_line_class, f):
        print("-----------------------", file=f)
        print("Time Table Line File", file=f)
        print("-----------------------", file=f)
        print(file=f)
        print(time_table_line_class.comment1, file=f)
        print(time_table_line_class.comment2, file=f)
        print(file=f)
        if time_table_line_class.userallowed:
            print("[userallowed]", file=f)
            print(file=f)
        print("[priority]", file=f)
        print(time_table_line_class.priority, file=f)
        if time_table_line_class.tours is not None:
            for tour in time_table_line_class.tours:
                print("------------------------------------", file=f)
                print(file=f)
                print("[newtour]", file=f)
                print(tour.tour_name, file=f)
                print(tour.ai_group_name, file=f)
                print(tour.line3, file=f)
                print(file=f)
                print("------------------------------------", file=f)
                print(file=f)
                if tour.trips is not None:
                    for trip in tour.trips:
                        print(trip.comment, file=f)
                        print("[addtrip]", file=f)
                        print(trip.trip_name, file=f)
                        print(trip.line2, file=f)
                        print(trip.depart_time, file=f)
                        print(file=f)
