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

EMPTY_STR = ''

print("OMSI Map Merger "+version.version)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class GuiGroupManager:
    pass

class MapsListManager(GuiGroupManager):
    def __init__(self,
                 omsi_map_merger: omsi_map_merger.OmsiMapMerger,
                 gui,
                 window,
                 key_listbox: str,
                 key_add_input: str,
                 key_add_button: str,
                 key_remove: str,
                 key_status: str,
                 ):
        self.__omsi_map_merger: omsi_map_merger.OmsiMapMerger = omsi_map_merger
        self.__gui = gui
        self.__listbox = window[key_listbox]
        self.__input_add = window[key_add_input]
        self.__button_add = window[key_add_button]
        self.__button_remove = window[key_remove]
        self.__status_bar = window[key_status]
        self.__ready_to_confirm = False
    
    def ready_to_confirm(self) -> bool:
        return len(self.__omsi_map_merger.get_maps()) >= 2
    
    def __refresh_maps_list(self) -> None:
        self.__listbox.update(values=self.__omsi_map_merger.get_maps())

    def __handle_listbox(self) -> None:
        self.__button_remove.update(disabled=False)

    def __handle_add(self) -> None:
        try:
            self.__omsi_map_merger.append_map(self.__input_add.get())
            self.__refresh_maps_list()
            self.__button_remove.update(disabled=True)
            #self.__refresh_confirm()
        except ValueError as e:
            self.__gui.popup(e)
        except omsi_map_merger.MapRepetitionError as e:
            self.__gui.popup(e)
    
    def __handle_remove(self) -> None:
        self.__omsi_map_merger.remove_map(self.__listbox.get_indexes()[0])
        self.__refresh_maps_list()
        self.__button_remove.update(disabled=True)
        #self.__refresh_confirm()
    
    def enable(self) -> None:
        for gui_element in [self.__listbox, self.__input_add, self.__button_add]:
            gui_element.update(disabled=False)
        self.__status_bar.update(value="NOT COMPLETED", background_color=None)
        
        self.__refresh_maps_list()# TO JEST DO USUNIECIA RAZEM Z MAPAMI DO TESTOWANIA W OmsiMap.__init__ ALBO CO NAJMNIEJ DO PRZEMYŚLENIA
    
    def disable(self) -> None:
        for gui_element in [self.__listbox, self.__input_add, self.__button_add, self.__button_remove]:
            gui_element.update(disabled=True)
        self.__status_bar.update(value="CONFIRMED", background_color='green')
    
    def handle_event(self, event) -> None:
        for gui_element, handler in [
            (self.__listbox, self.__handle_listbox),
            (self.__input_add, self.__handle_add),
            (self.__button_remove, self.__handle_remove),
        ]:
            if gui_element.key == event:
                handler()
                return True
        return False

class MapLoadingInteractionManager(GuiGroupManager):
    def __init__(self,
                 omsi_map_merger: omsi_map_merger.OmsiMapMerger,
                 gui,
                 window: sg.Window,
                 key_tree: str,
                 key_details: str,
                 key_load_whole_maps: str,
                 key_load_selected: str,
                 ) -> None:
        self.__omsi_map_merger: omsi_map_merger.OmsiMapMerger = omsi_map_merger
        self.__gui = gui
        self.__tree: gui.Tree = window[key_tree]
        self.__multiline_details: gui.Multiline = window[key_details]
        self.__button_load_whole_map: gui.Button = window[key_load_whole_maps]
        self.__button_load_selected: gui.Button = window[key_load_selected]
    
    def ready_to_confirm(self) -> bool:
        return False

    def __update_tree(self):
        tree_data: sg.TreeData = sg.TreeData()
        for omsi_map in map(lambda x: x.omsi_map, self.__omsi_map_merger.get_maps()):
            tree_data.insert(EMPTY_STR, omsi_map, str(omsi_map.get_directory()), ["MAP", str(omsi_map.fully_loaded())])
            for tree_row in [
                # Name, Type, SafeParser
                ("global.cfg", "GC", omsi_map.get_global_config()),
                ("timetable/", "TT", omsi_map.get_standard_timetable()),
                ("ailists.cfg", "AILISTS", omsi_map.get_ailists()),
            ]:
                tree_data.insert(omsi_map, tree_row[2], tree_row[0], [tree_row[1], tree_row[2].info_short()])
            
            tree_data.insert(omsi_map, omsi_map.get_tiles(), "Tiles", [EMPTY_STR, EMPTY_STR])
            for tile in omsi_map._map:
                tree_data.insert(omsi_map.get_tiles(), tile, "some tile", ["TILE", tile.info_short()])
        self.__tree.update(values = tree_data)
    
    def enable(self) -> None:
        for gui_element in [
            #self.__tree,# can't be disabled
            self.__button_load_whole_map,
            self.__button_load_selected,
        ]:
            gui_element.update(disabled=False)
        self.__update_tree()
    
    def disable(self) -> None:
        pass

    def __handle_tree(self) -> None:
        try:
            self.__multiline_details.update(value=self.__tree.SelectedRows[0].info_detailed())
        except:
            self.__multiline_details.update(value="wybierz tam, gdzie jest info")
    
    def __handle_load_whole_map(self) -> None:
        self.__omsi_map_merger.load_maps()
    
    def __handle_load_selected(self) -> None:
        print(self.__tree.SelectedRows)#pass#if isinstance(,
        self.__tree.SelectedRows[0].load()
        self.__update_tree()
    
    def handle_event(self, event) -> bool:
        for gui_element, handler in [
            (self.__tree, self.__handle_tree),
            (self.__button_load_whole_map, self.__handle_load_whole_map),
            (self.__button_load_selected, self.__handle_load_selected),
        ]:
            if gui_element.key == event:
                handler()
                return True
        return False
        return False

class GuiGroupToManage:
    def __init__(self,
                 gui_group_manager: GuiGroupManager,
                 window,
                 key_button_next_group: str,
        ) -> None:
        self.gui_group_manager: GuiGroupManager = gui_group_manager
        self.button_next_group = window[key_button_next_group]

class GuiGroupsManager:
    def __init__(self,
                 groups_to_manage: list[GuiGroupToManage],
                 ) -> None:
        if len(groups_to_manage) == 0:
            raise ValueError(f"At least one GuiGroupToManage  is required (provided 0).")
        self.__groups_to_manage: list[GuiGroupToManage] = groups_to_manage
        self.__groups_iter: list_iterator = iter(self.__groups_to_manage)
        self.__current_group = next(self.__groups_iter)
        self.__current_group.gui_group_manager.enable()
    
    def __switch_to_next_group(self):
        self.__current_group.button_next_group.update(disabled=True)
        self.__current_group.gui_group_manager.disable()
        self.__current_group = next(self.__groups_iter)
        self.__current_group.button_next_group.update(disabled=False)
        self.__current_group.gui_group_manager.enable()
    
    def dalej(self):
        self.__switch_to_next_group()# to jest nie do używania i do skasowania

    def handle_event(self, key: str) -> bool:
        if key == self.__current_group.button_next_group.key:
            self.__switch_to_next_group()
            return True
        elif self.__current_group.gui_group_manager.handle_event(key):
            self.__current_group.button_next_group.update(disabled = not self.__current_group.gui_group_manager.ready_to_confirm())
            return True
        return False

directories_layout = [
    [sg.Text("Select directories of maps you want to merge. (at least 2)")],
    [sg.Listbox([], size=(70,5), disabled=True, key='maps_directories', enable_events=True)],
    [
        sg.Input(visible=False, enable_events=True, key='maps_directories_add_input', disabled=True),
        sg.FolderBrowse("Add", key='maps_directories_add_button', disabled=True),
        sg.Button("Remove", key='maps_directories_remove', disabled=True),
    ],
    [
        sg.Button("Confirm selected maps directories", key="maps_directories_confirm", disabled=True),
        sg.Text("Directory selection status: "),
        sg.StatusBar("NOT COMPLETED", key='maps_directories_status')],
    ]

map_reading_panel = [
    [sg.Button("Read whole maps", key="load_whole_maps", disabled=True), sg.Text("Maps reading status: "), sg.StatusBar("trudno powiedzieć")],
    [sg.Tree(sg.TreeData(),
             ["Type", "Status"],
             col0_heading="Name",
             num_rows=20,
             enable_events=True,
             key="load_tree",
             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
             col0_width=40,
             auto_size_columns=False,
             col_widths=[10,20],
             )
    ],
    [
        sg.Button("Load_selected", key="load_selected", disabled=True),
        sg.Button("Open text editor", key="open_text_editor", disabled=True),
    ],
    [sg.Multiline(key='load_details', s=(90,10), disabled=True, default_text="det")],
    [sg.Button("Confirm load", key="load_confirm", disabled=True)]
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

omm = omsi_map_merger.OmsiMapMerger()
window = sg.Window("OMSI Map Merger", layout, finalize=True)

maps_list_manager = MapsListManager(omm,
                                    sg,
                                    window,
                                    'maps_directories',
                                    'maps_directories_add_input',
                                    'maps_directories_add_button',
                                    'maps_directories_remove',
                                    'maps_directories_status',
                                    )

maps_loading_interaction_manager: MapLoadingInteractionManager = MapLoadingInteractionManager(
    omm,
    sg,
    window,
    'load_tree',
    'load_details',
    'load_whole_maps',
    'load_selected')

gui_groups_manager: GuiGroupsManager = GuiGroupsManager(
    [
        GuiGroupToManage(maps_list_manager, window, 'maps_directories_confirm'),
        GuiGroupToManage(maps_loading_interaction_manager, window, 'load_confirm'),
    ]
)
gui_groups_manager.dalej()###

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == "cancel":
        break
    elif gui_groups_manager.handle_event(event):
        pass
    #trzeba kiedyś ustawić raise exception jak jest event nieobsłużony
    
    print(f"GUI event occured: {event}, values: {values}")
window.close()
