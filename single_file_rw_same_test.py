# Copyright 2025 Bartosz Gajewski
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

import pytest
import _pytest.mark.structures as pytest_structures
import pathlib
import os
import filecmp

import global_config_parser
import global_config_serializer
import busstops_parser
import busstops_serializer
import station_links_parser
import station_links_serializer
import time_table_line_parser
import time_table_line_serializer
import track_parser
import track_serializer
import trip_parser
import trip_serializer
import chrono_tile_parser
import chrono_tile_serializer

rw_params: list[pytest_structures.ParameterSet] = []
try:
    test_maps_dir: pathlib.Path = pathlib.Path(os.environ['OMM_TEST_MAPS_DIRECTORY'])
except KeyError:
    pass
else:
    for file_type_name, parser, serializer, file_patterns in [
        ('GC', global_config_parser.GlobalConfigParser, global_config_serializer.GlobalConfigSerializer, ['*/global.cfg']),
        ('BUSSTOPS', busstops_parser.BusstopsParser, busstops_serializer.BusstopsSerializer, ['*/TTData/Busstops.cfg', '*/Chrono/*/TTData/Busstops.cfg']),
        ('STN-LINKS', station_links_parser.StationLinksParser, station_links_serializer.StationLinksSerializer, ['*/TTData/StnLinks.cfg', '*/Chrono/*/TTData/StnLinks.cfg']),
        ('TTLINE', time_table_line_parser.TimeTableLineParser, time_table_line_serializer.TimeTableLineSerializer, ['*/TTData/*.ttl', '*/Chrono/*/TTData/*.ttl']),
        ('TRACK', track_parser.TrackParser, track_serializer.TrackSerializer, ['*/TTData/*.ttr', '*/Chrono/*/TTData/*.ttr']),
        ('TRIP', trip_parser.TripParser, trip_serializer.TripSerializer, ['*/TTData/*.ttp', '*/Chrono/*/TTData/*.ttp']),
        ('CHRONO-TILE', chrono_tile_parser.ChronoTileParser, chrono_tile_serializer.ChronoTileSerializer, ['*/Chrono/*/tile_*_*.map']),
    ]:
        for file_pattern in file_patterns:
            for path in test_maps_dir.glob(file_pattern):
                rw_params.append(pytest.param(parser, serializer, path, id=f"{file_type_name}: {path.relative_to(test_maps_dir)}"))
    rw_params.sort(key=lambda param: str(param.id)) # must be sorted for pytest-xdist

@pytest.mark.parametrize("parser_class, serializer_class, source_file", rw_params)
def test_rw_same(parser_class, serializer_class, source_file: pathlib.Path, tmp_path: pathlib.Path):
    p = parser_class()
    s = serializer_class()
    result_file: pathlib.Path = tmp_path / source_file.parts[-1]
    s.serialize(p.parse(str(source_file)), str(result_file))
    assert filecmp.cmp(source_file, result_file), f"File \"{result_file}\" is not same as \"{source_file}\"."
    