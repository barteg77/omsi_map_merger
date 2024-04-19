# Copyright 2020, 2021, 2023, 2024 Bartosz Gajewski
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
import traceback
import omsi_map
import omsi_map_merger
import global_config_parser
import version
import loader
import timetable

EMPTY_STR = ''

print("OMSI Map Merger", version.version)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class MapLoadingInteractionManager:
    class NoSelectedMapComponentError(Exception):
        pass

    def __init__(self,
                 merger: omsi_map_merger.OmsiMapMerger,
                 gui,
                 window: sg.Window,
                 key_tree: str,
                 key_details: str,
                 key_add_input: str,
                 key_add_button: str,
                 key_remove: str,
                 key_load_whole_maps: str,
                 key_load_selected: str,
                 key_load_scan_chronos: str,
                 key_load_scan_timetable_lines: str,
                 key_load_scan_tracks: str,
                 key_load_scan_trips: str,
                 ) -> None:
        self.__omsi_map_merger: omsi_map_merger.OmsiMapMerger = merger
        self.__gui = gui
        self.__tree: gui.Tree = window[key_tree]
        self.__multiline_details: gui.Multiline = window[key_details]
        self.__input_add: gui.Button = window[key_add_input]
        self.__button_add: gui.Button = window[key_add_button]
        self.__button_remove: gui.Button = window[key_remove]
        self.__button_load_whole_map: gui.Button = window[key_load_whole_maps]
        self.__button_load_selected: gui.Button = window[key_load_selected]
        self.__button_load_scan_chronos: gui.Button = window[key_load_scan_chronos]
        self.__button_load_scan_timetable_lines = window[key_load_scan_timetable_lines]
        self.__button_load_scan_tracks = window[key_load_scan_tracks]
        self.__button_load_scan_trips = window[key_load_scan_trips]
        self.__maps_components_by_id = dict() #add type hint (int, anything)

        self.__update_tree()
        self.__update_disability()
    
    def ready_to_confirm(self) -> bool:
        return False

    def __update_tree(self):
        tree_data: sg.TreeData = sg.TreeData()
        self.__maps_components_by_id = dict()

        def add_to_tree(parent_map_component, element_map_component, name: str, component_type: str, status: str) -> None:
            self.__maps_components_by_id[id(element_map_component)] = element_map_component
            tree_data.insert(EMPTY_STR if parent_map_component == EMPTY_STR  else id(parent_map_component),
                             id(element_map_component),
                             name,
                             [component_type, status],
                            )
        def add_safe_loader(parent_component, safe_loader: loader.SafeLoader):
            for loader_type, add_function in [
                (loader.SafeLoaderUnit, add_safe_loader_unit),
                (loader.SafeLoaderList, add_safe_loader_list),
            ]:
                if isinstance(safe_loader, loader_type):
                    add_function(parent_component, safe_loader)
                    return
            raise Exception(f"This object isn't object of SafeLoader type (is  {type(safe_loader).__name__})")
        
        def add_safe_loader_unit(parent_component, loader_unit: loader.SafeLoaderUnit):
            add_to_tree(parent_component, loader_unit, loader_unit.get_name(), "unit/"+loader_unit.get_type(), loader_unit.info_short())

        def add_safe_loader_list(parent_component, loader_list: loader.SafeLoaderList):
            add_to_tree(parent_component, loader_list, loader_list.get_name(), "list", loader_list.info_short())
            for loader in loader_list.get_data():
                add_safe_loader(loader_list, loader)
        
        for map_to_merge in self.__omsi_map_merger.get_maps():
            om = map_to_merge.omsi_map
            add_safe_loader(EMPTY_STR, om)
        
        self.__tree.update(values = tree_data)

    def __get_selected_map_component(self):
        try:
            return self.__maps_components_by_id[self.__tree.SelectedRows[0]]
        except IndexError:
            raise self.NoSelectedMapComponentError()

    def __handle_tree(self) -> None:
        try:
            self.__multiline_details.update(value=self.__get_selected_map_component().info_detailed())
        except (AttributeError,# 'MapToMerge' object has no attribute 'info_detailed' // to wyrzucić jak będą tylko SafeLoadery w tree
                self.NoSelectedMapComponentError,# After removal of map to merge, 'load_tree' event occurs,
                                                 # but there is no selected map component. (Tree data was updated.)
                ):
            self.__multiline_details.update(value="wybierz tam, gdzie jest info\n" + traceback.format_exc())
    
    def __handle_add(self) -> None:
        try:
            self.__omsi_map_merger.append_map(self.__input_add.get())
            self.__update_tree()
            #self.__button_remove.update(disabled=True)
        except ValueError as e:
            self.__gui.popup(e)# "x" is not directory
        except omsi_map_merger.MapRepetitionError as e:
            self.__gui.popup(e)
    
    def __handle_remove(self) -> None:
        self.__omsi_map_merger.remove_map(self.__omsi_map_merger.get_maps().index(self.__get_selected_map_component()))
        self.__update_tree()
        #self.__button_remove.update(disabled=True)
    
    def __handle_load_selected(self) -> None:
        try:
            smc = self.__get_selected_map_component()
        except self.NoSelectedMapComponentError:
            raise self.NoSelectedMapComponentError(f"Handling of \"Load selected\" is allowed only when SafeLoader (or its derivative) is selected. There is nothing selected.")
        
        if isinstance(smc, loader.SafeLoader):
            self.__get_selected_map_component().load()
        elif isinstance(smc, list):# list of SafeLoaders
            for component in smc:
                component.load()
        else:
            raise self.NoSelectedMapComponentError(f"Handling of \"Load selected\" is allowed only when SafeLoader (or its derivative) is selected. Type of selected: {type(smc)}.")
            
        self.__update_tree()
        #self.__update_disability() może to jest potrzebne pomyslec kiedyś
    
    def __is_selected_component_instance(self, component_type) -> bool:
        try:
            return isinstance(self.__get_selected_map_component(), component_type)
        except self.NoSelectedMapComponentError:
            return False
    
    def __update_disability(self):
        self.__button_remove.update(disabled = not self.__is_selected_component_instance(omsi_map_merger.MapToMerge))
        self.__button_load_scan_chronos.update(disabled = not (self.__is_selected_component_instance(omsi_map_merger.MapToMerge)
                            and self.__get_selected_map_component().omsi_map.get_global_config().get_status() == loader.FileParsingStatus.READ_SUCCESS))
        self.__button_load_selected.update(disabled = not (   self.__is_selected_component_instance(loader.SafeLoader)
                                                           or self.__is_selected_component_instance(list)
                                                           ))
        self.__button_load_whole_map.update(disabled = not len(self.__omsi_map_merger.get_maps()))
        selected_tt = self.__is_selected_component_instance(timetable.Timetable)
        for button in [
            self.__button_load_scan_timetable_lines,
            self.__button_load_scan_tracks,
            self.__button_load_scan_trips,
        ]:
            button.update(disabled = not selected_tt)
    
    def handle_event(self, event) -> bool:
        if self.__tree.key == event:
            self.__handle_tree()#needn't tree update
            self.__update_disability()
            return True
        for gui_element, handler in [
            (self.__input_add, self.__handle_add),
            (self.__button_remove, self.__handle_remove),
            (self.__button_load_whole_map, lambda: self.__omsi_map_merger.load_maps()),
            (self.__button_load_selected, self.__handle_load_selected),
            (self.__button_load_scan_chronos, lambda: self.__get_selected_map_component().omsi_map.scan_chrono()),#po co to jest w lambda??
            (self.__button_load_scan_timetable_lines, lambda: self.__get_selected_map_component().scan_time_table_lines()),
            (self.__button_load_scan_tracks, lambda: self.__get_selected_map_component().scan_tracks()),
            (self.__button_load_scan_trips, lambda: self.__get_selected_map_component().scan_trips()),
        ]:
            if gui_element.key == event:
                handler() # need tree update
                self.__update_tree()
                self.__update_disability()
                return True
        return False

map_reading_panel = [
    [
        sg.Input(visible=False, enable_events=True, key='load_add_input', disabled=True),
        sg.FolderBrowse("Add", key='load_add_button'),
        sg.Button("Remove", key='load_remove'),
        sg.Button("Read whole maps", key='load_whole_maps', disabled=True),
    ],
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
    [
        sg.Button("Scan for chronos", key='load_scan_chronos', disabled=True),
        sg.Button("Scan for lines", key='load_scan_timetable_lines', disabled=True),
        sg.Button("Scan for tracks", key='load_scan_tracks', disabled=True),
        sg.Button("Scan for trips", key='load_scan_trips', disabled=True),
    ],
    [sg.Multiline(key='load_details', s=(90,10), disabled=True, default_text="det")],
]

layout_left = [
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

maps_loading_interaction_manager: MapLoadingInteractionManager = MapLoadingInteractionManager(
    omm,
    sg,
    window,
    'load_tree',
    'load_details',
    'load_add_input',
    'load_add_button',
    'load_remove',
    'load_whole_maps',
    'load_selected',
    'load_scan_chronos',
    'load_scan_timetable_lines',
    'load_scan_tracks',
    'load_scan_trips')

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == "cancel":
        break
    elif maps_loading_interaction_manager.handle_event(event):
        pass
    #trzeba kiedyś ustawić raise exception jak jest event nieobsłużony
    
    #print(f"GUI event occured: {event}, values: {values}")
window.close()
