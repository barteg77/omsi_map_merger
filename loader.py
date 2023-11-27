# Copyright 2023 Bartosz Gajewski
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

from enum import Enum

class Loader:
    def __init__(self):
        self.data = None

class FileParsingStatus(Enum):
    NOT_READ = 1
    READ_SUCCESS = 2
    ERROR = 3

class SafeLoader:
    def __init__(self, real_loader) -> None:
        self.__real_loader: Loader = real_loader
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception: Exception = None
    
    def get_status(self) -> FileParsingStatus:
        return self.__status
    
    def get_data(self) -> None:
        if self.__status == FileParsingStatus.READ_SUCCESS:
            return self.__real_loader.data
        else:
            raise NoDataError(f"Unable to return data, file parsing status is {self.__status}.")
    
    def load(self) -> None:
        print(type(self.__real_loader).__name__, "loading file...")
        try:
            self.__real_loader.load()
            self.__status = FileParsingStatus.READ_SUCCESS
            self.__exception  = None
        except Exception as exception:
            self.__status = FileParsingStatus.ERROR
            self.__exception = exception
    
    def info_short(self) -> str:
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "NOT READ"
            case FileParsingStatus.READ_SUCCESS:
                return "READ SUCCESSFULLY"
            case FileParsingStatus.ERROR:
                return f"ERROR: {type(self.__exception).__name__}"
    
    def info_detailed(self) -> str:
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "File not read yet."
            case FileParsingStatus.READ_SUCCESS:
                return "Loaded successfully."
            case FileParsingStatus.ERROR:
                return str(self.__exception)