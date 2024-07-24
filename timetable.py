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
import named_data as nd
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

class Timetable:
    def __init__(self,
                 tbusstops: busstops.Busstops,
                 tstation_links: station_links.StationLinks,
                 ttime_table_lines: list[nd.NamedData[time_table_line.TimeTableLine]],
                 ttracks: list[nd.NamedData[track.Track]],
                 ttrips: list[nd.NamedData[trip.Trip]],
    ):
        self.busstops: busstops.Busstops = tbusstops
        self.station_links: station_links.StationLinks = tstation_links
        self.time_table_lines: list[nd.NamedData[time_table_line.TimeTableLine]] = ttime_table_lines
        self.tracks: list[nd.NamedData[track.Track]] = ttracks
        self.trips: list[nd.NamedData[trip.Trip]] = ttrips

class TimetableSl(loader.SafeLoaderList):
    def __init__(self,
                 map_directory: str,
                 chrono_directory: str = "",
                 ):
        self.map_directory = map_directory
        self.chrono_directory = chrono_directory
        self.busstops = loader.SafeLoaderUnit(busstops.Busstops, os.path.join(self.map_directory, self.chrono_directory, "TTData", "Busstops.cfg"), _busstops_parser.parse)
        self.station_links = loader.SafeLoaderUnit(station_links.StationLinks, os.path.join(self.map_directory, self.chrono_directory, "TTData", "StnLinks.cfg"), _station_links_parser.parse)
        self.time_table_line_files = []
        self.time_table_lines: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable lines")
        self.scanned_time_table_lines: bool = False
        self.track_files = []
        self.tracks: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable tracks")
        self.scanned_tracks: bool = False
        self.trip_files = []
        self.trips: loader.SafeLoaderList = loader.SafeLoaderList([], "Timetable trips")
        self.scanned_trips: bool = False
        super().__init__([
            self.time_table_lines,
            self.tracks,
            self.trips,
            self.busstops,
            self.station_links,
        ], "Timetable")
    
    def get_pure(self) -> Timetable:
        if not self.ready():
            raise loader.NoDataError
        
        return Timetable(self.busstops.get_data(),
                             self.station_links.get_data(),
                             [nd.NamedData(*args) for args in zip(self.time_table_line_files, [sl.get_data() for sl in self.time_table_lines.get_data()])],
                             [nd.NamedData(*args) for args in zip(self.track_files, [sl.get_data() for sl in self.tracks.get_data()])],
                             [nd.NamedData(*args) for args in zip(self.trip_files, [sl.get_data() for sl in self.trips.get_data()])],
        )

    
    def scan_time_table_lines(self) -> None:
        self.time_table_line_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttl"))]
        self.time_table_lines.set_data(list(map(lambda time_table_line_file: loader.SafeLoaderUnit(time_table_line.TimeTableLine, os.path.join(self.map_directory, self.chrono_directory, "TTData", time_table_line_file), _time_table_line_parser.parse), self.time_table_line_files)))
        self.scanned_time_table_lines  = True
    
    def scan_tracks(self) -> None:
        self.track_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttr"))]
        self.tracks.set_data(list(map(lambda track_file: loader.SafeLoaderUnit(track.Track, os.path.join(self.map_directory, self.chrono_directory, "TTData", track_file), _track_parser.parse), self.track_files)))
        self.scanned_tracks = True
    
    def scan_trips(self) -> None:
        self.trip_files = [os.path.relpath(x, os.path.join(self.map_directory, self.chrono_directory, "TTData")) for x in glob.glob(os.path.join(self.map_directory, self.chrono_directory, "TTData", "*.ttp"))]
        self.trips.set_data(list(map(lambda trip_file: loader.SafeLoaderUnit(trip.Trip, os.path.join(self.map_directory, self.chrono_directory, "TTData", trip_file), _trip_parser.parse), self.trip_files)))
        self.scanned_trips = True
    
    def load(self):
        self.scan_time_table_lines()
        self.scan_tracks()
        self.scan_trips()
        super().load()
    
    def everything_scanned(self) -> bool:
        return self.scanned_time_table_lines and self.scanned_tracks and self.scanned_trips

    def ready(self) -> bool:
        return super().ready() and self.everything_scanned()
    
    def scanned_info(self) -> str:
        component_type_name_scanned: list[tuple[str, bool]] = [
            ("TTL", self.scanned_time_table_lines),
            ("TTR", self.scanned_tracks),
            ("TTP", self.scanned_trips),
        ]
        not_scanned_names: list[str] = [component[0] for component in component_type_name_scanned if not component[1]]
        return f"{' and '.join(not_scanned_names)} not scanned!\n" if not self.everything_scanned() else ""
    
    def info_detailed(self) -> str:
        return self.scanned_info() + super().info_detailed()
    
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
