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

class NoDataError(Exception):
    pass

class Loader:
    def __init__(self):
        self.data = None

class FileParsingStatus(Enum):
    NOT_READ = 1
    READ_SUCCESS = 2
    OPTIONAL_NOT_EXISTS = 3
    ERROR = 4

class SafeLoader:
    def __init__(self,
                 real_loader,
                 callback_loaded: callable = None,
                 callback_failed: callable = None,
                 optional: bool = False,
                 ) -> None:
        self.__real_loader: Loader = real_loader
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception: Exception = None
        self.__callback_loaded: function
        if bool(callback_loaded is None) ^ bool(callback_failed is None):
            raise Exception("You have to provide callback_loaded and callback_failed or not to provide any of them.")
        self.__callback_loaded: callable = callback_loaded if callback_loaded is not None else lambda: None
        self.__callback_failed: callable = callback_failed if callback_failed is not None else lambda: None
        self.__optional = optional
    
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
            self.__exception = None
            self.__callback_loaded()
        except Exception as exception:
            if self.__optional and isinstance(exception, FileNotFoundError):
                self.__status = FileParsingStatus.OPTIONAL_NOT_EXISTS
                return
            self.__status = FileParsingStatus.ERROR
            self.__exception = exception
            self.__callback_failed()
    
    def info_short(self) -> str:
        match self.__status:
            case FileParsingStatus.NOT_READ:
                return "NOT READ"
            case FileParsingStatus.READ_SUCCESS:
                return "READ SUCCESSFULLY"
            case FileParsingStatus.OPTIONAL_NOT_EXISTS:
                return "NOT EXISTS (optional)"
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