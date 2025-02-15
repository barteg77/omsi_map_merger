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
import pathlib
import filecmp
import omsi_map
import os
import pathlib
import _pytest.mark.structures as pytest_structures
import ailists
import ailists_parser
import itertools

maps_dirs: list[pytest_structures.ParameterSet]
try:
    maps_dirs = [pytest.param(map_path, id=map_path.parts[-1]) for map_path in sorted(pathlib.Path(os.environ['OMM_TEST_MAPS_DIRECTORY']).iterdir()) if map_path.is_dir()]
except KeyError:
    maps_dirs = []

@pytest.mark.parametrize("source_map_dir", maps_dirs)
def test_map_rw(source_map_dir: pathlib.Path, tmp_path: pathlib.Path):
    # read map, save and chceck if are same
    safe_loader: omsi_map.OmsiMapSl = omsi_map.OmsiMapSl(str(source_map_dir))
    safe_loader.load()
    test_map: omsi_map.OmsiMap = safe_loader.get_data()
    result_map_dir: pathlib.Path = tmp_path
    test_map.save(str(result_map_dir))

    requied_files_patterns: list[str] = [
        'global.cfg',
        # ailists.cfg not listed here because it isn't expected to be exactly same,
        # (comments are omitted while parsing)
        'drivers.txt',
        'Holidays.txt',
        'humans.txt',
        'parklist_p.txt',
        'registrations.txt',
        'signalroutes.cfg',
        'texture/water.tga',
        'texture/water_bump.bmp',
        'texture/water_envmap.bmp',
        'unsched_trafficdens.txt',
        'unsched_vehgroups.txt',
        'picture.jpg',
        'timezone.txt',
        'TTData/*.tt[lpr]',
        'Chrono/*/Chrono.cfg'
        'Chrono/*/TTData/*.tt[lpr]',
    ] + list(itertools.chain.from_iterable([[ # for each tile
            f'{map_file}',
            f'{map_file}.terrain',
            f'{map_file}.water',
            f'{map_file}.LM.bmp',
            f'{map_file}.roadmap.bmp',
            f'texture/map/{map_file}.roadmap.bmp',
            f'texture/map/{map_file}.*.dds',
            f'Chrono/*/{map_file}',
        ] for map_file in map(lambda map_entry: map_entry.map_file, test_map.global_config._map)]))

    for pattern in requied_files_patterns:
        for source_file in source_map_dir.glob(pattern):
            result_file: pathlib.Path = result_map_dir / source_file.relative_to(source_map_dir)
            assert filecmp.cmp(source_file, result_file), f"File \"{result_file}\" is not same as \"{source_file}\"."
    
    # ailists consistency test:
    # data in saved result ailists must be same as in source ailists
    ap: ailists_parser.AIListsParser = ailists_parser.AIListsParser()
    parsed_result_ailists: ailists.AILists = ap.parse(str(result_map_dir / 'ailists.cfg'))
    assert test_map.ailists == parsed_result_ailists, "Result ailists data differ from source ailists data"
