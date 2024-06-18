# Copyright 2024 Bartosz Gajewski
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
import omsi_map_merger
import global_config

@pytest.fixture
def some_entrypoint() -> global_config.Entrypoints:
    # 1 is entrypoint object id
    # 6 is index of tile with entrypoint
    # "Test entrypoint" is entrypoint's name
    # '88' means this value is irrelevant
    return global_config.Entrypoints('88', 1, '88', '88', '88', '88', '88', '88', '88', '88', 6, "Test entrypoint")

def test_shifted_entrypoint(some_entrypoint) -> None:
    se: global_config.Entrypoints = omsi_map_merger.shifted_entrypoint(some_entrypoint, 10000, 2)
    assert int(se.id) == 10001
    assert int(se.tile_index) == 8

def test_shifted_entrypoints(some_entrypoint) -> None:
    shift_idcode: int = 12
    shift_tile_index: int = 34
    assert omsi_map_merger.shifted_entrypoints([some_entrypoint], shift_idcode, shift_tile_index) == \
        [omsi_map_merger.shifted_entrypoint(some_entrypoint, shift_idcode, shift_tile_index)]

@pytest.fixture
def some_gc_tile() -> global_config.Map:
    pos_x: int = 12
    pos_y: int = 34
    return global_config.Map(pos_x,
                             pos_y,
                             f'tile_{pos_x}_{pos_y}.map')

def test_shifted_gc_tile(some_gc_tile) -> None:
    shifted: global_config.Map = omsi_map_merger.shifted_gc_tile(some_gc_tile, 11, 22)
    assert shifted.pos_x == 23
    assert shifted.pos_y == 56
    assert shifted.map_file == 'tile_23_56.map'

def test_shifted_gc_tiles(some_gc_tile) -> None:
    shift_x: int = 1234
    shift_y: int = 5678
    assert omsi_map_merger.shifted_gc_tiles([some_gc_tile], shift_x, shift_y) == \
        [omsi_map_merger.shifted_gc_tile(some_gc_tile, shift_x, shift_y)]