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
import loader

class SomethingToLoad:
    def __init__(self):
        pass

def something_loader(path: str) -> SomethingToLoad:
    return SomethingToLoad()

@pytest.fixture
def basic_slu():
    return loader.SafeLoaderUnit(SomethingToLoad,
                                "file path",
                                something_loader)

def test_get_data_before_read(basic_slu):
    with pytest.raises(loader.NoDataError):
        basic_slu.get_data()

def test_get_type_name(basic_slu):
    assert basic_slu.get_type_name() == SomethingToLoad.__name__

def test_set_external_data(basic_slu):
    stl = SomethingToLoad()
    basic_slu.set_external_data(stl)
    assert basic_slu.get_status() is loader.FileParsingStatus.EXTERNAL_DATA
    assert basic_slu.ready()
    assert basic_slu.get_data() is stl

class SomeError(Exception):
    pass

def failing_true_loader(path: str):
    raise SomeError("some error message")

@pytest.fixture
def basic_slu_fail():
    return loader.SafeLoaderUnit(SomethingToLoad,
                                "file path",
                                failing_true_loader)

def test_get_data_after_fail(basic_slu_fail):
    basic_slu_fail.load()
    with pytest.raises(loader.NoDataError):
        basic_slu_fail.get_data()

def test_get_status_after_fail(basic_slu_fail):
    basic_slu_fail.load()
    assert basic_slu_fail.get_status() == loader.FileParsingStatus.ERROR

def test_detailed_error_info(basic_slu_fail):
    basic_slu_fail.load()
    assert SomeError.__name__ in basic_slu_fail.info_detailed(), "error's type name not present"
    assert "some error message" in str(basic_slu_fail.info_detailed()), "error message not present"
