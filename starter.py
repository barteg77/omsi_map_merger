# Copyright 2020, 2021, 2023 Bartosz Gajewski
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

import PySimpleGUI as sg
import os
import omsi_map_merger
import global_config_parser
import version

print("OMSI Map Merger "+version.version)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

omm = omsi_map_merger.OmsiMapMerger()

class MapsListManager:
    def __init__(self,
                 omsi_map_merger: omsi_map_merger.OmsiMapMerger,
                 window,
                 gui,
                 key_listbox: str,
                 key_add_input: str,
                 key_add_button: str,
                 key_remove: str,
                 key_confirm: str,
                 key_status: str,
                 ):
        self.__omsi_map_merger: omsi_map_merger.OmsiMapMerger = omsi_map_merger
        self.__gui = gui
        self.__listbox = window[key_listbox]
        self.__input_add = window[key_add_input]
        self.__button_add = window[key_add_button]
        self.__button_remove = window[key_remove]
        self.__button_confirm = window[key_confirm]
        self.__status_bar = window[key_status]
    
    def __refresh_maps_list(self):
        self.__listbox.update(values=self.__omsi_map_merger.get_maps())
    
    def __refresh_confirm(self):
        self.__button_confirm.update(disabled = len(self.__omsi_map_merger.get_maps()) < 2)

    def __handle_listbox(self):
        self.__button_remove.update(disabled=False)

    def __handle_add(self):#write 'void'
        try:
            self.__omsi_map_merger.append_map(self.__input_add.get())
            self.__refresh_maps_list()
            self.__button_remove.update(disabled=True)
            self.__refresh_confirm()
        except ValueError as e:
            self.__gui.popup(e)
        except omsi_map_merger.MapRepetitionError as e:
            self.__gui.popup(e)
    
    def __handle_remove(self):
        self.__omsi_map_merger.remove_map(self.__listbox.get_indexes()[0])
        self.__refresh_maps_list()
        self.__button_remove.update(disabled=True)
        self.__refresh_confirm()
    
    def __handle_confirm(self):
        for gui_element in [self.__listbox, self.__input_add, self.__button_add, self.__button_remove, self.__button_confirm]:
            gui_element.update(disabled=True)
        self.__status_bar.update(value="CONFIRMED", background_color='green')
        #now enable map reading section
    
    def handle_event(self, event):
        for gui_element, handler in [
            (self.__listbox, self.__handle_listbox),
            (self.__input_add, self.__handle_add),
            (self.__button_remove, self.__handle_remove),
            (self.__button_confirm, self.__handle_confirm),
        ]:
            if gui_element.key == event:
                handler()
                return True
        return False

treedata = sg.TreeData()
treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
treedata.Insert("", '_B_', 'B', [])
treedata.Insert("_A_", '_A1_', '✅Sb I\ntem 1', ['can', 'be', 'anything'], )

directories_layout = [
    [sg.Text("Select directories of maps you want to merge. (at least 2)")],
    [sg.Listbox([], size=(70,5), key='maps_directories', enable_events=True)],
    [
        sg.Input(visible=False, enable_events=True, key='maps_directories_add_input'),
        sg.FolderBrowse("Add", key='maps_directories_add_button'),
        sg.Button("Remove", key='maps_directories_remove', disabled=True),
    ],
    [
        sg.Button("Confirm selected maps directories", key="maps_directories_confirm", disabled=True),
        sg.Text("Directory selection status: "),
        sg.StatusBar("NOT COMPLETED", key='maps_directories_status')],
    ]

file_details = sg.Multiline(s=(15,10), disabled=True, default_text="det")
map_reading_panel = [
    [sg.Button("Read whole maps", key="read_whole_maps", disabled=True), sg.Text("Maps reading status: "), sg.StatusBar("trudno powiedzieć")],
    [sg.Tree(treedata, ["Type", "Path", "Status"], num_rows=20, enable_events=True, key="maps_tree")],
    [
        sg.Button("Parse file", key="parse_file"),
        sg.Button("Open text editor", key="open_text_editor"),
    ],
    [file_details],
]

layout_left = [
    [sg.Frame("Select maps to merge", directories_layout)],
    [sg.Frame("Reading maps files", map_reading_panel)],
]

layout_right = [
    [sg.Text("Set map 2 shift…"),],
    [sg.Graph(canvas_size=(640, 640), graph_bottom_left=(-320,-320), graph_top_right=(320, 320), background_color="white", key="graph")],
    [sg.Button("    ←    ", key="shift_left"),
        sg.Button("    ↑    ", key="shift_up"),
        sg.Button("    ↓    ", key="shift_down"),
        sg.Button("    →    ", key="shift_right"),
        sg.Text("Colours:"),
        sg.Text(" MAP1 ", text_color="black", background_color="yellow"),
        sg.Text(" MAP2 ", text_color="white", background_color="green"),
        sg.Text(" BOTH MAPS ", text_color="white", background_color="red")],
    [sg.HorizontalSeparator(),],
    [sg.Checkbox("Keep original main ground texture on tiles of Map 2 if are not same", key="keep_map2_groundtex"),],
    [sg.Text("New map directory"),sg.In(key="new_map_directory"), sg.FolderBrowse()],
    [sg.Button("Merge maps!", key="merge"), sg.Button("Cancel", key="cancel")]
]
layout = [[sg.Column(layout_left), sg.VSep(), sg.Column(layout_right)]]
_global_config_parser = global_config_parser.GlobalConfigParser()
map1_last_directory = None
map2_last_directory = None
gc1 = None
gc2 = None
gc1_set = None
gc2_set = None
min1_x = None
max1_x = None
min1_y = None
max1_y = None
min2_x = None
max2_x = None
min2_y = None
max2_y = None
shift_x = 0
shift_y = 0

def draw_scheme():
    global map1_last_directory
    global map2_last_directory
    global gc1
    global gc2
    global gc1_set
    global gc2_set
    global min1_x
    global max1_x
    global min1_y
    global max1_y
    global min2_x
    global max2_x
    global min2_y
    global max2_y
    global shift_x
    global shift_y
    if not map1_last_directory == values["map1_directory"]:
        gc1 = _global_config_parser.parse(os.path.join(os.path.realpath(values["map1_directory"]),"global.cfg"))
        map1_last_directory = values["map1_directory"]
        if (gc1.worldcoordinates):
            sg.popup('Map 1: Value of "worldcoordinates" is True.\nMap created during merge can be corrupted!')

        shift_x = None
        min1_x = min([int(tile.pos_x) for tile in gc1._map])
        max1_x = max([int(tile.pos_x) for tile in gc1._map])
        min1_y = min([int(tile.pos_y) for tile in gc1._map])
        max1_y = max([int(tile.pos_y) for tile in gc1._map])

        gc1_set = set([(int(tile.pos_x), int(tile.pos_y)) for tile in gc1._map])#tu ma byc  wciete bo to sie nie przesuwa

    draw_shift_x = int(min1_x + (max1_x - min1_x) / 2)
    draw_shift_y = int(min1_y + (max1_y - min1_y) / 2)

    if not map2_last_directory == values["map2_directory"]:
        gc2 = _global_config_parser.parse(os.path.join(os.path.realpath(values["map2_directory"]),"global.cfg"))
        map2_last_directory = values["map2_directory"]
        if (gc2.worldcoordinates):
            sg.popup('Map 2: Value of "worldcoordinates" is True.\nMap created during merge can be corrupted!')

        shift_x = None
        min2_x = min([int(tile.pos_x) for tile in gc2._map])
        max2_x = max([int(tile.pos_x) for tile in gc2._map])
        min2_y = min([int(tile.pos_y) for tile in gc2._map])
        max2_y = max([int(tile.pos_y) for tile in gc2._map])

    if shift_x == None:
        map2_middle_x = int(min2_x + (max2_x - min2_x) / 2)
        map2_middle_y = int(min2_y + (max2_y - min2_y) / 2)

        shift_x = draw_shift_x - map2_middle_x
        shift_y = draw_shift_y - map2_middle_y

    gc2_set = set([(int(tile.pos_x)+shift_x, int(tile.pos_y)+shift_y) for tile in gc2._map])#tu ma byc nie wciete bo to sie przesuwa
    
    tile_size = 5
    graph = window["graph"]
    graph.Erase()
    for tile_x, tile_y in gc1_set:
        tile_x -= draw_shift_x
        tile_y -= draw_shift_y
        graph.DrawRectangle((tile_x*tile_size, tile_y*tile_size),
                            ((tile_x+1)*tile_size, (tile_y+1)*tile_size),
                            line_color="black",
                            fill_color="yellow")
    for tile_x, tile_y in gc2_set:
        if (tile_x, tile_y) in gc1_set:
            tile_x -= draw_shift_x
            tile_y -= draw_shift_y
            graph.DrawRectangle((tile_x*tile_size, tile_y*tile_size),
                                ((tile_x+1)*tile_size, (tile_y+1)*tile_size),
                                line_color="black",
                                fill_color="red")
        else:
            tile_x -= draw_shift_x
            tile_y -= draw_shift_y
            graph.DrawRectangle((tile_x*tile_size, tile_y*tile_size),
                                ((tile_x+1)*tile_size, (tile_y+1)*tile_size),
                                line_color="black",
                                fill_color="green")

window = sg.Window("OMSI Map Merger", layout)
maps_list_manager = MapsListManager(omm,
                                    window,
                                    sg,
                                    'maps_directories',
                                    'maps_directories_add_input',
                                    'maps_directories_add_button',
                                    'maps_directories_remove',
                                    'maps_directories_confirm',
                                    'maps_directories_status')
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == "cancel":
        break
    elif maps_list_manager.handle_event(event):
        pass    
    elif event == "maps_tree":
        file_details.update(value="default_text")
    
    print(f"GUI event occured: {event}, values: {values}")
    """
    elif not os.path.isdir(values["map1_directory"]):
        sg.popup('"'+values["map1_directory"]+'" is not directory!', 'In "Map 1 directory" you must insert directory.')
    elif not os.path.isfile(os.path.join(values["map1_directory"], "global.cfg")):
        sg.popup('There is no flie "global.cfg" in Map 1 directory: "'+values["map1_directory"]+'".')
    elif not os.path.isdir(values["map2_directory"]):
        sg.popup('"'+values["map2_directory"]+'" is not directory!', 'In "Map 2 directory" you must insert directory.')
    elif not os.path.isfile(os.path.join(values["map2_directory"], "global.cfg")):
        sg.popup('There is no flie "global.cfg" in Map 2 directory: "'+values["map2_directory"]+'".')
    elif event == "shift_left":
        shift_x -= 1
        draw_scheme()
    elif event == "shift_up":
        shift_y += 1
        draw_scheme()
    elif event == "shift_down":
        shift_y -= 1
        draw_scheme()
    elif event == "shift_right":
        shift_x += 1
        draw_scheme()
    elif map1_last_directory != values["map1_directory"] or map2_last_directory != values["map2_directory"]:
        draw_scheme()
    elif event == "merge":
        if gc2_set is None:
            sg.popup("You must set map 2 shift.")
        else:
            overlap = False
            for tile_x, tile_y in gc2_set:
                if (tile_x, tile_y) in gc1_set:
                    overlap = True
                    break
            if not overlap:
                omsi_map_merger.merge(values["map1_directory"],
                                      values["map2_directory"],
                                      shift_x,
                                      shift_y,
                                      values["new_map_directory"],
                                      values["keep_map2_groundtex"])
                sg.popup("Done.")
            else:
                sg.popup("Maps can't overlap!")
    """
window.close()
