# OMSI Map Merger
This program merges two OMSI 2 maps creating a resulting map preserving as much information from source maps as possible. It allows to specify position of merged maps and preview their arrangement on a diagram
### OMSI Map Merger handles:
- Correct operating timetables of both merged maps in resulting map.
- Allows user to decide if main ground texture of second map should be added as a new layer that covers whole area of second map tiles effectively emulating different main ground texture on that area.
### Known restrictions:
- Syntax of source maps’ files should be matching from files created with OMSI 2 Editor (parsers are quite strict on that).
- Line (Time Table Line) names, track names and trip names should be unique in source maps – duplicates will be dropped.
- There cannot be text beyond sections declaring AI groups in `ailists.cfg` even though OMSI accepts it.
- Old-type ailists ([like this](https://forum.omnibussimulator.de/forum/index.php?thread/11880-tut-changing-adjusting-the-ai-list-ailist/)) files are not handled.
- Maps with enabled [worldcoordinates] aren't handled properly.
- `unsched_trafficdens.txt` and `unsched_vehgroups.txt` files are not handled.
- `global_*.dsc` files are not handled.
- `chrono_#upd.cfg` files in Chrono directories are not handled.
## Installation
OMSI Map Merger is distributed in two forms: standalone Windows executable and as python source.
### All-in-one on Windows
To run you have to extract package archive and run `omsi_map_merger/omsi_map_merger.exe`.
### Python source
To run you need Python 3.12 (or newer compatible) and have to install pip packages using this command: `pip install charset-normalizer==3.3.2 parglare==0.13.0 PySimpleGUI==4.70.1`.

Merger should be started by typing `python3 starter.py` in console.

## User Manual
See [english](MANUAL_en.md) or [polish](MANUAL_pl.md) user manual.