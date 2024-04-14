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

import os
import shutil
class OmsiFile:
    def __init__(self,
                 map_path="",
                 pattern="",
                 params=None,
                 optional=False,
                 real_file_name=None
                 ):
        self.map_path = map_path
        self.pattern = pattern
        self.params = params
        self.optional = optional
        if real_file_name is None:
            self.real_file_name = os.path.realpath(os.path.join(self.map_path, self.get_file_name()))
        else:
            self.real_file_name = real_file_name
            
    def get_file_name(self):
        if self.params is None:
            return self.pattern
        return self.pattern.format(**self.params)
    
    def save(self,
             target_directory=""
             ):
        real_target_file = os.path.realpath(os.path.join(target_directory, self.get_file_name()))
        if os.path.isfile(self.real_file_name):
            if not self.real_file_name == real_target_file:
                print("Copying file "+ self.real_file_name + " to " + real_target_file)
                shutil.copyfile(self.real_file_name, real_target_file)
            else:
                print("File " + self.real_file_name + " will not be copied to the same directory")
        elif self.optional:
            print("Optional file " + self.real_file_name + " does not exist, will not be copied.")
        else:
            print("Non-optional file " + self.real_file_name + " does not exist, will not be copied.")

class OmsiFiles:
    def __init__(self, omsi_files=None):
        self.omsi_files = omsi_files
        if self.omsi_files is None:
            self.omsi_files = []
    
    def add(self, omsi_file):
        self.omsi_files.append(omsi_file)
    
    def save(self,
             target_directory=""
             ):
        for of in self.omsi_files:
            of.save(target_directory)
    
    def get_files_names(self) -> list[str]:
        return [ofile.get_file_name() for ofile in self.omsi_files]
