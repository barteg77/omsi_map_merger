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
import logging

logger = logging.getLogger(__name__)

class OmsiFile:
    def __init__(self,
                 map_path,#="",
                 pattern,#="",
                 params: dict[str, str] = {},
                 optional=False,
                 real_file_name=None
                 ):
        self.map_path = map_path
        self.pattern = pattern
        self.params: dict[str, str] = params
        self.optional = optional
        if real_file_name is None:
            self.real_file_name = os.path.realpath(os.path.join(self.map_path, self.get_file_name()))
        else:
            self.real_file_name = real_file_name
            
    def get_file_name(self) -> str:
        if self.params is None:
            return self.pattern
        return self.pattern.format(**self.params)
    
    def save(self,
             target_directory=""
             ) -> None:
        real_target_file = os.path.realpath(os.path.join(target_directory, self.get_file_name()))
        if os.path.isfile(self.real_file_name):
            if not self.real_file_name == real_target_file:
                logger.info("Copying file "+ self.real_file_name + " to " + real_target_file)
                shutil.copyfile(self.real_file_name, real_target_file)
            else:
                logger.info("File " + self.real_file_name + " will not be copied to the same directory")
        elif self.optional:
            logger.info("Optional file " + self.real_file_name + " does not exist, will not be copied.")
        else:
            logger.info("Non-optional file " + self.real_file_name + " does not exist, will not be copied.")

class OmsiFiles:
    def __init__(self, omsi_files=[]):
        self.omsi_files = omsi_files
    
    def add(self, omsi_file) -> None:
        self.omsi_files.append(omsi_file)
    
    def save(self,
             target_directory=""
             ) -> None:
        for of in self.omsi_files:
            of.save(target_directory)
    
    def get_files_names(self) -> list[str]:
        return [ofile.get_file_name() for ofile in self.omsi_files]
    
    def set_omsi_files(self, ofiles: list[OmsiFile]) -> None:
        if type(ofiles) is not list:
            raise Exception(f"You must provide list[OmsiFile] here (provided {type(ofiles)}.")
        for ofile in ofiles:
            if type(ofile) is not OmsiFile:
                raise Exception(f"You must provide list[OmsiFile] here (one of list's elements is {type(ofile)}.")
        self.omsi_files = ofiles