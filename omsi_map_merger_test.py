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
import itertools
import omsi_map_merger
import global_config
import tile

# "global.cfg" realted tests

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

# "tile_x_y.map" related tests
@pytest.fixture
def some_tile() -> tile.Tile:
    return tile.Tile("Created for testing purposes",
                     '14',
                     True, True, True, True,
                     [
                         tile.Spline(False, '0', 'Splines\\Marcel\\Hstr_6spur_Wilhelm1.sli', 4, 0,5,'45.8954123576869','3.81469718101361E-6','14.8770606207205','0','149.999997646012','199.99999686135', \
                                     '0','0','0','0','0','0','0','',False, None,[]),
                     ],
                     [
                         tile._Object('Object Nr. 1',False, '0','Sceneryobjects\\Buildings_MC\\bw_50s_01.sco',6,'53.3936693422588','126.708424359543','0','29.4639429430018','0','0','0',[], None, False, []),
                         tile.SplineAttachement('Object Nr. 0','0','Sceneryobjects\\Buildings_MC\\bw_30s_01.sco',1,'0','48.6367491077964','0','9.71228307628491','277.671388033057','0','0', \
                                                '29.9999995292025','299.999995292025','0','0',None, None, False, None),
                         tile.SplineAttachementRepeater('Object Nr. 23','0','12','117','Sceneryobjects\\Dodatkowe busze Heir\\Busz 4a\\Busz 4_5m.sco', 10989,'0','-3.52011121533649',\
                                                        '-0.499999992153375','971.351040613941','90.0000020235813','0','0','2.99999995292025','394.999998955127','0', '0', None, 4444, False, None),
                     ])

def test_tile_shifted_id_natural(some_tile) -> None:
    def all_ids(t:tile.Tile) -> list[int]:
        sli_ids: list[int] = list(itertools.chain.from_iterable([(sli.id, sli. id_previous, sli.id_next) for sli in t.spline]))
        sco_ids: list[int] = list(itertools.chain.from_iterable([tuple([sco.id]) if sco.varparent is None else (sco.id, sco.varparent) for sco in t._object]))
        return sli_ids + sco_ids
    
    #print(all_ids(some_tile))
    id_shift: int = 63897
    shifted: tile.Tile = omsi_map_merger.tile_shifted_ids(some_tile, id_shift)
    assert all_ids(shifted) == [id + id_shift if id != 0 else 0 for id in all_ids(some_tile)]

def test_tile_shifted_id_0(some_tile) -> None:
    assert some_tile == omsi_map_merger.tile_shifted_ids(some_tile, 0)
