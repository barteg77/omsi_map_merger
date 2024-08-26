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

import tile
import typing

class Select:
    def __init__(self,
                 spline: bool,
                 id: int,
                 lines: list[str]):
        self.spline: bool = spline
        self.id: int = id
        self.lines: list[str] = lines

class ChronoTile:
    def __init__(self,
                 initial_comment: str,
                 version: str,
                 elements_list: list[Select | tile.Spline | tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater],
                 ):
        self.initial_comment: str = initial_comment
        self.version: str = version
        self.elements_list: list[Select | tile.Spline | tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater] = elements_list

    def change_ids(self, value: int) -> None:
        for entry in self.elements_list:
            entry.id += value
            if type(entry) == tile.Spline:
                entry.id_previous += value
                entry.id_next += value
            elif any(map(lambda valid_type: type(entry) == valid_type, [tile._Object, tile.SplineAttachement, tile.SplineAttachementRepeater])):
                entry_object: tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater \
                    = typing.cast(tile._Object | tile.SplineAttachement | tile.SplineAttachementRepeater, entry)
                if entry_object.varparent is not None:
                    entry_object.varparent += value
