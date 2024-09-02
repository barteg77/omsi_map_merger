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

import platform
import os
import pathlib
import subprocess

class FENFError(Exception):
    pass

def supported() -> bool:
    return platform.system() == 'Windows'

def run_explorer_windows(select_file: pathlib.Path) -> None:
    assert platform.system() == 'Windows'
    windir: str | None = os.getenv('WINDIR')
    if windir is None:
        raise FENFError("env. var. 'WINDIR' doesn't exists")
    else:# windir is string for sure
        explorer_path: pathlib.Path = pathlib.Path(windir) / 'explorer.exe' # type: ignore
        subprocess.run([str(explorer_path), f'/select,{select_file}'])

def run_explorer_sel(selected_path: pathlib.Path) -> None:
    assert supported()
    run_explorer_windows(selected_path)
