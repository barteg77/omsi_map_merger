# Copyright 2020, 2023, 2024 Bartosz Gajewski
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

import time_table_line
import time_table_line_parser
import time_table_line_serializer
import track
import track_parser
import track_serializer
import trip
import trip_parser
import trip_serializer
import busstops
import busstops_parser
import busstops_serializer
import station_links
import station_links_parser
import station_links_serializer
import loader
import glob
import os

_time_table_line_parser = time_table_line_parser.TimeTableLineParser()
_time_table_line_serializer = time_table_line_serializer.TimeTableLineSerializer()

_track_parser = track_parser.TrackParser()
_track_serializer = track_serializer.TrackSerializer()

_trip_parser = trip_parser.TripParser()
_trip_serializer = trip_serializer.TripSerializer()

_busstops_parser = busstops_parser.BusstopsParser()
_busstops_serializer = busstops_serializer.BusstopsSerializer()

_station_links_parser = station_links_parser.StationLinksParser()
_station_links_serializer = station_links_serializer.StationLinksSerializer()

class TimetableLineLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.data = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: time_table_line.TimeTableLine = _time_table_line_parser.parse(self.path)

class TrackLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.data = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: track.Track = _track_parser.parse(self.path)

class TripLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.data = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: trip.Trip = _trip_parser.parse(self.path)

class BusstopsLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.data = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: busstops.Busstops = _busstops_parser.parse(self.path)

class StationLinksLoader(loader.Loader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.data = None
        #self.__path: str = path
    
    def load(self) -> None:
        self.data: station_links.StationLinks = _station_links_parser.parse(self.path)

class Timetable:
    def __init__(self,
                 map_directory: str,
                 chrono_directory: str = "",
                 ):
        self.map_directory = map_directory
        self.chrono_directory = chrono_directory
        self.busstops = loader.SafeLoaderUnit(BusstopsLoader(os.path.join(self.map_directory, self.chrono_directory, "TTData", "Busstops.cfg")))
        self.station_links = loader.SafeLoaderUnit(StationLinksLoader(os.path.join(self.map_directory, self.chrono_directory, "TTData", "StnLinks.cfg")))
        self.time_table_line_files = []
        self.time_table_lines: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable lines")
        self.track_files = []
        self.tracks: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable tracks")
        self.trip_files = []
        self.trips: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable trips")
    
    def scan_time_table_lines(self) -> None:
        self.time_table_line_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttl"))]
        self.time_table_lines = loader.SafeLoaderList(list(map(lambda time_table_line_file: loader.SafeLoaderUnit(TimetableLineLoader(os.path.join(self.map_directory, self.chrono_directory, "TTData", time_table_line_file))), self.time_table_line_files)), self.time_table_lines.get_name())
    
    def scan_tracks(self) -> None:
        self.track_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttr"))]
        self.tracks = loader.SafeLoaderList(list(map(lambda track_file: loader.SafeLoaderUnit(TrackLoader(os.path.join(self.map_directory, self.chrono_directory, "TTData", track_file))), self.track_files)), self.tracks.get_name())
    
    def scan_trips(self) -> None:
        self.trip_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttp"))]
        self.trips = loader.SafeLoaderList(list(map(lambda trip_file: loader.SafeLoaderUnit(TripLoader(os.path.join(self.map_directory, self.chrono_directory, "TTData", trip_file))), self.trip_files)), self.trips.get_name())
    
    def load(self):
        self.scan_time_table_lines()
        self.scan_tracks()
        self.scan_trips()
        for safe_loader_list in [self.time_table_lines, self.tracks, self.trips]:
            safe_loader_list.load()
        
        for safe_loader in [self.busstops, self.station_links]:
            safe_loader.load()
    
    def save(self):
        for time_table_line, time_table_line_file in zip(self.time_table_lines, self.time_table_line_files):
            print("Serializing time table file " + os.path.join(self.map_directory, self.chrono_directory, "TTData", time_table_line_file))
            _time_table_line_serializer.serialize(time_table_line, os.path.join(self.map_directory, self.chrono_directory, "TTData", time_table_line_file))
        
        for track, track_file in zip(self.tracks, self.track_files):
            print("Serializing track file " + os.path.join(self.map_directory, self.chrono_directory, "TTData", track_file))
            _track_serializer.serialize(track, os.path.join(self.map_directory, self.chrono_directory, "TTData", track_file))
        
        for trip, trip_file in zip(self.trips, self.trip_files):
            print("Serializing trip file " + os.path.join(self.map_directory, self.chrono_directory, "TTData", trip_file))
            _trip_serializer.serialize(trip, os.path.join(self.map_directory, self.chrono_directory, "TTData", trip_file))
        
        print("Serializing busstops file " + os.path.join(self.map_directory, self.chrono_directory, "TTData", "Busstops.cfg"))
        _busstops_serializer.serialize(self.busstops, os.path.join(self.map_directory, self.chrono_directory, "TTData", "Busstops.cfg"))
        
        print("Serializing station links file " + os.path.join(self.map_directory, self.chrono_directory, "TTData", "StnLinks.cfg"))
        _station_links_serializer.serialize(self.station_links, os.path.join(self.map_directory, self.chrono_directory, "TTData", "StnLinks.cfg"))
    
    def change_ids_and_tile_indexes(self, ids_value, tile_indexes_value):
        print("Changing objects' IDs and tiles' indexes in tracks.")
        for track in self.tracks:
            track.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
        
        print("Changing objects' IDs and tiles' indexes in trips.")
        for trip in self.trips:
            trip.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
        
        print("Changing objects' IDs, splines' IDs and tiles' indexes in Busstops.cfg file.")
        self.busstops.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
        
        print("Changing objects' IDs, splines' IDs and tiles' indexes in StnLinks.cfg file.")
        self.station_links.change_ids_and_tile_indexes(ids_value, tile_indexes_value)
