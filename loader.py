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
import logging

logger = logging.getLogger(__name__)

class NoDataError(Exception):
    pass

class FileParsingStatus(Enum):
    NOT_READ = auto()
    READ_SUCCESS = auto()
    OPTIONAL_NOT_EXISTS = auto()
    ERROR = auto()
    LOWER_MIXED = auto()

class SafeLoader:# BASE CLASS, DO NOT INSTANTIATE
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
    
    #def get_data(self):
    #    raise NotImplementedError()
    
    def get_omsi_files(self) -> omsi_files.OmsiFiles:
        return self.__omsi_files
    
    def omsi_files_info(self) -> str:
        return "Attached omsi-files:" + "".join(["\n\t"+ filename for filename in self.get_omsi_files().get_files_names()])
    
    def info_short(self) -> str:
        status_text: dict[FileParsingStatus, str] = {
            FileParsingStatus.NOT_READ: "NOT READ",
            FileParsingStatus.READ_SUCCESS: "READ SUCCESSFULLY",
            FileParsingStatus.OPTIONAL_NOT_EXISTS: "NOT EXISTS (optional)",
            FileParsingStatus.ERROR: "ERROR",
            FileParsingStatus.LOWER_MIXED: "MIXED",
        }
        return status_text[self.get_status()]
    
    def load(self) -> None:
        raise NotImplementedError()
    
    def ready(self) -> bool:
        raise NotImplementedError

class SafeLoaderUnit[T](SafeLoader):
    __placeholder_exception: Exception = Exception("placeholder exception")
    def __init__(self,
                 data_type: typing.Type[T],
                 path: str,
                 true_loader: typing.Callable[[str], T],
                 callback_loaded: typing.Callable[[], None] = lambda: None,
                 callback_failed: typing.Callable[[], None] = lambda: None,
                 ofiles: omsi_files.OmsiFiles = omsi_files.OmsiFiles(),
                 optional: bool = False,
                 ) -> None:
        super().__init__(ofiles)
        self.__data_type: typing.Type[T] = data_type
        self.__path: str = path
        self.__true_loader: typing.Callable[[str]] = true_loader
        self.__status: FileParsingStatus = FileParsingStatus.NOT_READ
        self.__exception: Exception = self.__placeholder_exception
        #assert bool(callback_loaded == (lambda: None)) != bool(callback_failed == (lambda: None)), "You have to provide callback_loaded and callback_failed or not to provide any of them."
        self.__callback_loaded: typing.Callable[[], None] = callback_loaded
        self.__callback_failed: typing.Callable[[], None] = callback_failed
        self.__optional: bool = optional
        self.__data: T
    
    def get_type_name(self) -> str:
        return self.__data_type.__name__
    
    def get_path(self) -> str:
        return self.__path

    def get_name(self) -> str:
        return os.path.split(self.get_path())[1]
    
    def get_status(self) -> FileParsingStatus:
        return self.__status
    
    def get_data(self) -> T:
        if self.__status is FileParsingStatus.READ_SUCCESS:
            return self.__data
        else:
            raise NoDataError(f"Unable to return data, file parsing status is {self.__status}.")
    
    def load(self) -> None:
        logger.info(f"SafeLoaderUnit of {self.__data_type.__name__} loading file \"{self.get_path()}\"...")
        try:
            loaded = self.__true_loader(self.get_path())
        except Exception as exception:
            if self.__optional and isinstance(exception, FileNotFoundError):
                    self.__status = FileParsingStatus.OPTIONAL_NOT_EXISTS
            else:
                logger.info("An error occured while loading\n" + traceback.format_exc())
                self.__status = FileParsingStatus.ERROR
                self.__exception = exception
                self.__callback_failed()
        else:
            assert type(loaded) == self.__data_type, f"true_loader must return object of type declared when constructing SafeLoader, required type: {self.__data_type}, type of returned: {type(loaded)}"
            self.__data = loaded
            self.__status = FileParsingStatus.READ_SUCCESS
            self.__exception = self.__placeholder_exception
            self.__callback_loaded()
        
        logger.info(f"Safe loading finished. Status set to {self.get_status()}")
    
    def info_detailed(self) -> str:
        status_description: str
        match self.__status:
            case FileParsingStatus.NOT_READ:
                status_description = "File not read yet."
            case FileParsingStatus.READ_SUCCESS:
                status_description = "Loaded successfully.\n" + repr(self.get_data())
                #return "Loaded successfully.\n" + repr(self.get_data())
            case FileParsingStatus.ERROR:
                status_description = f"Error: {type(self.__exception).__name__}\nError message: {str(self.__exception)}"
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
    
    def get_sl_list(self) -> list[SafeLoader]:
        return self.__lower_safe_loaders
    
    def set_sl_list(self, new_list: list[SafeLoader]) -> None:
        self.__lower_safe_loaders = new_list
    
    def load(self) -> None:
        for sl in self.__lower_safe_loaders:
            sl.load()
    
    def info_detailed(self) -> str:
        return "list of SafeLoaders\n" + self.omsi_files_info()
    
    def ready(self) -> bool:
        return all([sl.ready() for sl in self.get_sl_list()])