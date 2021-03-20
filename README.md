# OMSI Map Merger
This program merges two OMSI 2 maps creating a resulting map preserving as much information from source maps as possible. It allows to interactively specify position of second map relative to first one before merge process (there is a picture, which presents arrangement of map tiles after merge). Created map will be ready to use in simulator and will be named according to the pattern *NAME1 & NAME2*.
### OMSI Map Merger handles:
- Correct operating timetables of both merged maps in resulting map.
- Allows user to decide if main ground texture of second map should be added as a new layer that covers whole area of second map tiles effectively emulating different main ground texture on that area.
- Uniqueness of  AI vehicles groups names.
### Known restrictions:
- Syntax of source maps’ files should be matching from files created with OMSI 2 Editor (parsers are quite strict on that).
- Line (Time Table Line) names, track names and trip names should be unique in source maps – duplicates will be dropped.
- There cannot be text beyond sections declaring AI groups in `ailists.cfg` even though OMSI accepts it.
- `unsched_trafficdens.txt` and `unsched_vehgroups.txt` files are not handled.
- `global_*.dsc` files are not handled.
- `chrono_#upd.cfg` files in Chrono directories are not handled.
## Installation
OMSI Map Merger is distributed in two forms: standalone Windows executable and as python source.
### All-in-one on Windows
To run you have to extract package archive and run `omsi_map_merger/omsi_map_merger.exe`.
### Python source
To run you need Python 3 (tested on 3.8) with following additional packages: parglare, PySimpleGUI and charset_normalizer.
In this case merger should be started using `python3 starter.py` from console.
