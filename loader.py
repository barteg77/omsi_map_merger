# Copyright 2023, 2024 Bartosz Gajewski
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

from enum import Enum, auto
import typing
import os.path
import omsi_files
import traceback

class NoDataError(Exception):
    pass

class Loader:
    def __init__(self, path: str, ltype = "unknown"):
        self.type: str = ltype
        self.path: str = path
        self.data = None
    
    def get_type(self) -> str:
        return self.type

    def get_path(self) -> str:
        return self.path
    
    def load(self) -> None:
        raise NotImplementedError()
    
    # function self.load

class FileParsingStatus(Enum):
    NOT_READ = auto()
    READ_SUCCESS = auto()
    OPTIONAL_NOT_EXISTS = auto()
    ERROR = auto()#only SafeLoaderUnit can set this status!
    LOWER_MIXED = auto()

class SafeLoader:
    # function self.__init__
    # function self.get_status
    # function self.get_data
    # function self.load
    # function self.info_short
    # function self.info_detailed
    # self.object_specific_actions ????
    

    def __init__(self, ofiles: omsi_files.OmsiFiles) -> None:
        self.__omsi_files: omsi_files.OmsiFiles = ofiles
    
    def get_status(self) -> FileParsingStatus:
        raise NotImplementedError()
    
    def get_omsi_files(self) -> omsi_files.OmsiFiles:
        return self.__omsi_files
    
    def omsi_files_info(self) -> str:
        return "Attached omsi-files:" + "".join(["\n\t"+ filename for filename in self.get_omsi_files().get_files_names()])
    
    def info_short(self) -> str:
        status = self.get_status()
        match status:
            case FileParsingStatus.NOT_READ:
                return "NOT READ"
            case FileParsingStatus.READ_SUCCESS:
                return "READ SUCCESSFULLY"
            case FileParsingStatus.OPTIONAL_NOT_EXISTS:
                return "NOT EXISTS (optional)"
            case FileParsingStatus.ERROR:
                return f"ERROR"
            case FileParsingStatus.LOWER_MIXED:
                return "MIXED"
            case _:
                raise Exception(f"Unable to create short info for this status (is{status}).")
    
    def load(self) -> None:
        raise NotImplementedError()
    
    def ready(self) -> bool:
        raise NotImplementedError

class SafeLoaderUnit(SafeLoader):
    __placeholder_exception: Exception = Exception("placeholder exception")
    def __init__(self,
                 real_loader: Loader,
                 callback_loaded: typing.Callable[[], None] = lambda: None,
                 callback_failed: typing.Callable[[], None] = lambda: None,
                 ofiles: omsi_files.OmsiFiles = omsi_files.OmsiFiles(),
                 optional: bool = False,
                 ) -> None:
        super().__init__(ofiles)
        self.__real_loader: Loader = real_loader
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception: Exception = self.__placeholder_exception
        #assert bool(callback_loaded == (lambda: None)) != bool(callback_failed == (lambda: None)), "You have to provide callback_loaded and callback_failed or not to provide any of them."
        self.__callback_loaded: typing.Callable[[], None] = callback_loaded
        self.__callback_failed: typing.Callable[[], None] = callback_failed
        self.__optional = optional
    
    def get_type(self) -> str:
        return self.__real_loader.get_type()
    
    def get_path(self) -> str:
        return self.__real_loader.get_path()

    def get_name(self) -> str:
        return os.path.split(self.get_path())[1]
    
    def get_status(self) -> FileParsingStatus:
        return self.__status
    
    def get_data(self) -> typing.Any:
        if self.__status == FileParsingStatus.READ_SUCCESS:
            return self.__real_loader.data
        else:
            raise NoDataError(f"Unable to return data, file parsing status is {self.__status}.")
    
    def load(self) -> None:
        print(f"SafeLoaderUnit of {type(self.__real_loader).__name__} loading file \"{self.get_path()}\"...")
        try:
            self.__real_loader.load()
            self.__status = FileParsingStatus.READ_SUCCESS
            self.__exception = self.__placeholder_exception
            self.__callback_loaded() # type: ignore
        except Exception as exception:
            print(traceback.format_exc())
            if self.__optional and isinstance(exception, FileNotFoundError):
                    self.__status = FileParsingStatus.OPTIONAL_NOT_EXISTS
                    return
            self.__status = FileParsingStatus.ERROR
            self.__exception = exception
            self.__callback_failed() # type: ignore
        print(f"Safe loading finished. Status set to {self.get_status()}")
    
    def info_detailed(self) -> str:
        status_description: str
        match self.__status:
            case FileParsingStatus.NOT_READ:
                status_description = "File not read yet."
            case FileParsingStatus.READ_SUCCESS:
                status_description = "Loaded successfully.\n" + repr(self.get_data())
                #return "Loaded successfully.\n" + repr(self.get_data())
            case FileParsingStatus.ERROR:
                status_description = str(self.__exception)
            case FileParsingStatus.OPTIONAL_NOT_EXISTS:
                status_description = "This file does not exist, but it is not a problem, because it is optional."
            case _:
                raise Exception(f"This status was not expected here (is {self.__status})")
        return status_description + "\n" + self.omsi_files_info()
    
    def ready(self) -> bool:
        return self.get_status() in [FileParsingStatus.READ_SUCCESS, FileParsingStatus.OPTIONAL_NOT_EXISTS]
    
class SafeLoaderList(SafeLoader):
    def __init__(self,
                 sl_list: list[SafeLoader],
                 name: str,
                 ofiles: omsi_files.OmsiFiles = omsi_files.OmsiFiles(),
                 ) -> None:
        super().__init__(ofiles)
        if not (type(sl_list) == list and all([isinstance(sl, SafeLoader) for sl in sl_list])):
            raise Exception(f"\"sl_list\" must be list of SafeLoaders, is {repr(sl_list)}")
        self.__lower_safe_loaders: list[SafeLoader] = sl_list
        self.__name = name
    
    def get_status(self) -> FileParsingStatus:
        prev_status: FileParsingStatus = FileParsingStatus.ERROR
        try:
            prev_status = self.__lower_safe_loaders[0].get_status()
        except IndexError:
            return FileParsingStatus.READ_SUCCESS
        for sl in self.__lower_safe_loaders:
            if sl.get_status() != prev_status:
                return FileParsingStatus.LOWER_MIXED
        return prev_status
    
    def get_name(self) -> str:
        return self.__name
    
    def get_data(self) -> list[SafeLoader]:
        return self.__lower_safe_loaders
    
    def set_data(self, new_data: list[SafeLoader]) -> None:
        self.__lower_safe_loaders = new_data
    
    def load(self) -> None:
        for sl in self.__lower_safe_loaders:
            sl.load()
    
    def info_detailed(self) -> str:
        return "list of SafeLoaders\n" + self.omsi_files_info()
    
    def ready(self) -> bool:
        return all([sl.ready() for sl in self.get_data()])