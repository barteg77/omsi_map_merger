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

class AddTrip:
    def __init__(self,
                 comment,
                 trip_name,
                 line2,
                 depart_time):
        self.comment = comment
        self.trip_name = trip_name
        self.line2 = line2
        self.depart_time = depart_time

class NewTour:
    def __init__(self,
                 tour_name,
                 ai_group_name,
                 line3,
                 trips=None):
        self.tour_name = tour_name
        self.ai_group_name = ai_group_name
        self.line3 = line3
        self.trips = trips

class TimeTableLine:
    def __init__(self,
                 comment1=None,
                 comment2=None,
                 userallowed=None,
                 priority=None,
                 tours=None):
        self.comment1 = comment1
        self.comment2 = comment2
        self.userallowed = userallowed
        self.priority = priority
        self.tours = tours
