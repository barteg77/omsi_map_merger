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
import omsi_map_merger
import version
import loader
import timetable
import traceback
import logging
import os
import platform
import sys
import tempfile
import pathlib
import time
import run_files_manager

root_logger = logging.getLogger()

# set up basic logger
log_format_str: str = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(format=log_format_str, encoding='utf-8', level=logging.DEBUG)

# save log to file
log_file_path: pathlib.Path = pathlib.Path(tempfile.gettempdir()) / f'omsi_map_merger_{time.strftime('%Y-%m-%d_%H:%M:%S')}.log'
logger_handler_file = logging.FileHandler(str(log_file_path))
logger_handler_file.setFormatter(logging.Formatter(log_format_str))
root_logger.addHandler(logger_handler_file)

# set up starter logger
logger = logging.getLogger(__name__)

EMPTY_STR = ''

logger.info(f"This is OMSI Map Merger {version.version}")
logger.info(f"Python version is {sys.version}")
logger.info(f"Platform is {platform.platform()}")
logger.info(f"Log is being saved to file: \"{log_file_path}\"")

class MapLoadingInteractionManager:
    class NoSelectedMapComponentError(Exception):
        pass

    def __init__(self,
                 merger: omsi_map_merger.OmsiMapMerger,
                 window: sg.Window,
                 key_tree: str,
                 key_details: str,
                 key_add_input: str,
                 key_add_button: str,
                 key_remove: str,
                 key_load_whole_maps: str,
                 key_load_selected: str,
                 key_load_open_file: str,
                 key_load_scan_chronos: str,
                 key_load_scan_timetable_lines: str,
                 key_load_scan_tracks: str,
                 key_load_scan_trips: str,
                 key_graph: str,
                 key_shift_left: str,
                 key_shift_right: str,
                 key_shift_up: str,
                 key_shift_down: str,
                 key_toggle_keep_groundtex: str,
                 key_new_map_directory: str,
                 key_new_map_name: str,
                 key_merge: str,
                 ) -> None:
        self.__omsi_map_merger: omsi_map_merger.OmsiMapMerger = merger
        self.__tree: sg.Tree = window[key_tree] # type: ignore
        self.__multiline_details: sg.Multiline = window[key_details] # type: ignore
        self.__input_add: sg.Input = window[key_add_input] # type: ignore
        self.__button_add: sg.Button = window[key_add_button] # type: ignore
        self.__button_remove: sg.Button = window[key_remove] # type: ignore
        self.__button_load_whole_map: sg.Button = window[key_load_whole_maps] # type: ignore
        self.__button_load_selected: sg.Button = window[key_load_selected] # type: ignore
        self.__button_load_open_editor: sg.Button = window[key_load_open_file] # type: ignore
        self.__button_load_scan_chronos: sg.Button = window[key_load_scan_chronos] # type: ignore
        self.__button_load_scan_timetable_lines: sg.Button = window[key_load_scan_timetable_lines] # type: ignore
        self.__button_load_scan_tracks: sg.Button = window[key_load_scan_tracks] # type: ignore
        self.__button_load_scan_trips: sg.Button = window[key_load_scan_trips] # type: ignore
        self.__graph: sg.Graph = window[key_graph] # type: ignore
        self.__button_shift_left: sg.Button = window[key_shift_left] # type: ignore
        self.__button_shift_right: sg.Button = window[key_shift_right] # type: ignore
        self.__button_shift_up: sg.Button = window[key_shift_up] # type: ignore
        self.__button_shift_down: sg.Button = window[key_shift_down] # type: ignore
        self.__button_toggle_keep_groundtex: sg.Button = window[key_toggle_keep_groundtex] # type: ignore
        self.__button_merge: sg.Button = window[key_merge] # type: ignore
        self.__input_new_map_directory: sg.In = window[key_new_map_directory] # type: ignore
        self.__input_new_map_name: sg.In = window[key_new_map_name] # type: ignore
        self.__maps_components_by_id = dict() #add type hint (int, anything)

        self.__update_tree()
        self.__update_disability()
        self.__draw_graph()
    
    def ready_to_confirm(self) -> bool:
        return False

    def __update_tree(self):
        tree_data: sg.TreeData = sg.TreeData()
        self.__maps_components_by_id = dict()

        def add_to_tree(parent_map_component, element_map_component, name: str, component_type: str, status: str, ready: str) -> None:
            self.__maps_components_by_id[id(element_map_component)] = element_map_component
            tree_data.insert(EMPTY_STR if parent_map_component == EMPTY_STR  else id(parent_map_component),
                             id(element_map_component),
                             name,
                             [component_type, status, ready],
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
            add_to_tree(parent_component, loader_unit, loader_unit.get_name(), "unit/"+loader_unit.get_type_name(), loader_unit.info_short(), str(loader_unit.ready()))

        def add_safe_loader_list(parent_component, loader_list: loader.SafeLoaderList):
            add_to_tree(parent_component, loader_list, loader_list.get_name(), "list", loader_list.info_short(), str(loader_list.ready()))
            for loader in loader_list.get_data():
                add_safe_loader(loader_list, loader)
        
        for map_to_merge in self.__omsi_map_merger.get_maps():
            add_safe_loader(EMPTY_STR, map_to_merge)
        
        self.__tree.update(values = tree_data)
        self.__update_multiline()

    def __get_selected_map_component(self):
        try:
            return self.__maps_components_by_id[self.__tree.SelectedRows[0]]
        except IndexError:
            raise self.NoSelectedMapComponentError()

    def __update_multiline(self) -> None:
        try:
            self.__multiline_details.update(value=self.__get_selected_map_component().info_detailed())
        except (self.NoSelectedMapComponentError):# because tree data was updated
            self.__multiline_details.update(value="Select map component to see detailed info.")
    
    def __handle_add(self) -> None:
        try:
            self.__omsi_map_merger.append_map(self.__input_add.get())
            self.__update_tree()
            #self.__button_remove.update(disabled=True)
        except ValueError as e:
            sg.popup(e)# "x" is not directory
        except omsi_map_merger.MapRepetitionError as e:
            sg.popup(e)
    
    def __handle_remove(self) -> None:
        self.__omsi_map_merger.remove_map(self.__omsi_map_merger.get_maps().index(self.__get_selected_map_component()))
        self.__omsi_map_merger.get_maps()[0].set_keep_groundtex(False)
        self.__update_tree()
        #self.__button_remove.update(disabled=True)
    
    def __handle_load_selected(self) -> None:
        try:
            smc = self.__get_selected_map_component()
        except self.NoSelectedMapComponentError:
            raise self.NoSelectedMapComponentError(f"Handling of \"Load selected\" is allowed only when SafeLoader (or its derivative) is selected. There is nothing selected.")
        
        if isinstance(smc, loader.SafeLoader):
            self.__get_selected_map_component().load()
        else:
            raise self.NoSelectedMapComponentError(f"Handling of \"Load selected\" is allowed only when SafeLoader (or its derivative) is selected. Type of selected: {type(smc)}.")
            
        self.__update_tree()
        #self.__update_disability() może to jest potrzebne pomyslec kiedyś
    
    def __handle_load_open_editor(self) -> None:
        assert platform.system() == 'Windows', "Startfile available only on Windows"
        os.startfile(self.__get_selected_map_component().get_path()) # type: ignore
    
    def __handle_merge(self) -> None:
        try:
            mr: omsi_map_merger.MergeResult = self.__omsi_map_merger.merged_omsi_map(self.__input_new_map_name.get())
        except:
            error_message: str = "An error occured while merge:\n" + traceback.format_exc()
            logger.error(error_message)
            sg.Popup(error_message, title="Error")
        if len(mr.warnings) == 0 or sg.popup_yes_no(f"\
There {"was a warning" if len(mr.warnings) == 1 else "were warnings"} reported during map merge:\n\
{"\n".join([f"\t*{warn}" for warn in mr.warnings])}\n\
Do you still want to save merged map?",
                                                    title="Map merge warnings") == "Yes":
            try:
                mr.merged_map.save(self.__input_new_map_directory.get())
                sg.Popup(f"Map saved in directory \"{self.__input_new_map_directory.get()}\"",
                         title="Map save completed")
            except:
                error_message: str = "An error occured while saving map:\n" + traceback.format_exc()
                logger.error(error_message)
                sg.Popup(error_message, title="Error")
    
    def __is_selected_component_instance(self, component_type) -> bool:
        try:
            return isinstance(self.__get_selected_map_component(), component_type)
        except self.NoSelectedMapComponentError:
            return False
    
    def __update_disability(self):
        selected_mtm: bool = self.__is_selected_component_instance(omsi_map_merger.MapToMerge)

        self.__button_remove.update(disabled = not selected_mtm)
        self.__button_load_scan_chronos.update(disabled = not (selected_mtm
                            and self.__get_selected_map_component().get_global_config().get_status() == loader.FileParsingStatus.READ_SUCCESS))
        self.__button_load_whole_map.update(disabled = not len(self.__omsi_map_merger.get_maps()))
        self.__button_load_selected.update(disabled = not self.__is_selected_component_instance(loader.SafeLoader))
        self.__button_load_open_editor.update(disabled = not (self.__is_selected_component_instance(loader.SafeLoaderUnit) and platform.system() == 'Windows'))
        selected_tt :bool = self.__is_selected_component_instance(timetable.TimetableSl)
        for button in [
            self.__button_load_scan_timetable_lines,
            self.__button_load_scan_tracks,
            self.__button_load_scan_trips,
        ]:
            button.update(disabled = not selected_tt)
        for button in [
            self.__button_shift_left,
            self.__button_shift_right,
            self.__button_shift_up,
            self.__button_shift_down,
        ]:
            button.update(disabled=not selected_mtm)
        self.__button_toggle_keep_groundtex.update(disabled = not (selected_mtm and self.__get_selected_map_component() is not self.__omsi_map_merger.get_maps()[0]))
        self.__button_merge.update(disabled = not self.__omsi_map_merger.ready())
    
    def update_md(self) -> None:
        self.__update_multiline()#needn't tree update
        self.__update_disability()
    
    def update_tdg(self) -> None:
        self.__update_tree()
        self.__update_disability()
        self.__draw_graph() #tylko na chwilę!!!!
    
    def update_dg(self) -> None:
        self.__update_disability()
        self.__draw_graph() #tylko na chwilę!!!!
    
    def handle_event(self, event) -> bool:# true if handled, false if didn't handled
        for gui_element, handler, updater in [
            # some handlers have to be lambda-encapsulated because they access map components' members, that are sometimes not accesible
            # e.g. self.__get_selected_map_component().scan_chrono() is accessible only when OmsiMapLoader is selected

            (self.__tree, lambda: None, self.update_md),

            (self.__input_add, self.__handle_add, self.update_tdg),
            (self.__button_remove, self.__handle_remove, self.update_tdg),
            (self.__button_load_whole_map, self.__omsi_map_merger.load_maps, self.update_tdg),
            (self.__button_load_selected, self.__handle_load_selected, self.update_tdg),
            (self.__button_load_scan_chronos, lambda: self.__get_selected_map_component().scan_chrono(), self.__update_tree),
            (self.__button_load_scan_timetable_lines, lambda: self.__get_selected_map_component().scan_time_table_lines(), self.__update_tree),
            (self.__button_load_scan_tracks, lambda: self.__get_selected_map_component().scan_tracks(), self.__update_tree),
            (self.__button_load_scan_trips, lambda: self.__get_selected_map_component().scan_trips(), self.__update_tree),

            (self.__button_load_open_editor, self.__handle_load_open_editor, lambda: None),
            (self.__button_shift_left, lambda: self.__get_selected_map_component().shift(shift_x = -1), self.update_dg),
            (self.__button_shift_right, lambda: self.__get_selected_map_component().shift(shift_x = 1), self.update_dg),
            (self.__button_shift_up, lambda: self.__get_selected_map_component().shift(shift_y = 1), self.update_dg),
            (self.__button_shift_down, lambda: self.__get_selected_map_component().shift(shift_y = -1), self.update_dg),
            (self.__button_toggle_keep_groundtex, lambda: self.__get_selected_map_component().toggle_keep_groundtex(), self.__draw_graph),

            (self.__button_merge, self.__handle_merge, lambda: None),
        ]:
            if gui_element.key == event:
                handler()
                updater()
                return True
        return False
    
    def __draw_graph(self) -> None:
        logger.info("Drawing graph...")
        try:
            colors: list[str] = ['green4', 'maroon1', 'navajo white', 'navy', 'gainsboro', 'firebrick2', \
                                 'DarkOliveGreen4', 'khaki2', 'purple1', 'turquoise2', 'SeaGreen1', 'aquamarine4', \
                                 'DarkGoldenrod1', 'dark slate gray', 'cornflower blue', 'gray', 'medium blue', 'magenta4', \
                                 'slate blue', 'slate gray', 'yellow']
            marking_color: str = 'black'
            maps: list[omsi_map_merger.MapToMerge] = self.__omsi_map_merger.get_maps()
            maps_colors: dict[omsi_map_merger.MapToMerge, str] = dict(zip(maps, colors))
            name_row_height: int = 16
            if len(maps) > len(colors):
                sg.popup("Can't draw graph, maps count exceed available colors' count.")
                self.__graph.Erase()
                return
            
            self.__graph.Erase()
            tile_size: int = 7
            for tile_pos, present_maps in self.__omsi_map_merger.get_graph_data().items():
                fill_color = maps_colors[present_maps[0]] if len(present_maps) == 1 else marking_color

                left_x: int = tile_pos.pos_x*tile_size
                top_y: int = tile_pos.pos_y*tile_size
                right_x: int = (tile_pos.pos_x-1)*tile_size
                bottom_y: int = (tile_pos.pos_y-1)*tile_size
                
                top_left: tuple[int, int] = (left_x, top_y)
                top_right: tuple[int, int] = (right_x, top_y)
                bottom_left: tuple[int, int] = (left_x, bottom_y)
                bottom_right: tuple[int, int] = (right_x, bottom_y)

                self.__graph.DrawRectangle(top_left,
                                           bottom_right,
                                           line_color=marking_color,
                                           fill_color=fill_color)
                # marking 'keep groundtex'
                if present_maps[0].get_keep_groundtex():
                    self.__graph.draw_line(top_left, bottom_right)
                    self.__graph.draw_line(top_right, bottom_left)
            
            for index, [[name, keep_groundtex], color] in enumerate(zip([(mtm.get_name(), mtm.get_keep_groundtex()) for mtm in maps], colors)):
                top_left: tuple[int, int] = (-320, 320-index*name_row_height)
                bottom_right: tuple[int, int] = (-200, 320-(index+1)*name_row_height)
                self.__graph.draw_rectangle(top_left, bottom_right, color, color)
                self.__graph.draw_text(name + (" (keep groundtex)" if keep_groundtex else EMPTY_STR), top_left, text_location=sg.TEXT_LOCATION_TOP_LEFT)

        except loader.NoDataError:
            self.__graph.draw_text("An error occured while drawing.\nSome data required to draw a graph is missing.", (-320, -320), text_location=sg.TEXT_LOCATION_BOTTOM_LEFT)

try:
    map_reading_panel = [
        [
            sg.Input(visible=False, enable_events=True, key='load_add_input', disabled=True),
            sg.FolderBrowse("Add", key='load_add_button'),
            sg.Button("Remove", key='load_remove'),
            sg.Button("Read whole maps", key='load_whole_maps', disabled=True),
        ],
        [sg.Tree(sg.TreeData(),
                ["Type", "Status", "Ready"],
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
            sg.Button("Open file in editor", key='load_open_file', disabled=True),
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
        [
            sg.Text("Log file:"),
            sg.In(str(log_file_path), disabled=True),
            sg.Button("Copy path to clipboard", key='copy_log_path'),
            sg.Button("Open location in file manager", key='open_log_location', disabled=not run_files_manager.supported())
        ],
        [sg.Frame("Reading maps files", map_reading_panel)],
    ]

    layout_right = [
        [sg.Text("Set map 2 shift…"),],
        [sg.Graph(canvas_size=(640, 640), graph_bottom_left=(-320,-320), graph_top_right=(320, 320), background_color="white", key="graph")],
        [sg.Button("    ←    ", key="shift_left"),
            sg.Button("    ↑    ", key="shift_up"),
            sg.Button("    ↓    ", key="shift_down"),
            sg.Button("    →    ", key="shift_right"),],
        [sg.Button("(toggle) Keep original main ground texture on tiles of selected map", key="toggle_keep_groundtex")],
        [sg.HorizontalSeparator(),],
        [sg.Text("New map directory"), sg.In(key="new_map_directory"), sg.FolderBrowse()],
        [sg.Text("New map name"), sg.In(key="new_map_name")],
        [sg.Button("Merge maps!", key="merge"), sg.Button("Cancel", key="cancel")]
    ]
    layout = [[sg.Column(layout_left), sg.VSep(), sg.Column(layout_right)]]

    omm = omsi_map_merger.OmsiMapMerger()
    window = sg.Window("OMSI Map Merger", layout, finalize=True)

    maps_loading_interaction_manager: MapLoadingInteractionManager = MapLoadingInteractionManager(
        omm,
        window,
        'load_tree',
        'load_details',
        'load_add_input',
        'load_add_button',
        'load_remove',
        'load_whole_maps',
        'load_selected',
        'load_open_file',
        'load_scan_chronos',
        'load_scan_timetable_lines',
        'load_scan_tracks',
        'load_scan_trips',
        'graph',
        'shift_left',
        'shift_right',
        'shift_up',
        'shift_down',
        'toggle_keep_groundtex',
        'new_map_directory',
        'new_map_name',
        'merge')

    while True:
        event, values = window.read() # type: ignore
        logger.debug(f"GUI event occured: {event}, values: {values}")
        if event == sg.WIN_CLOSED or event == "cancel":
            break
        elif event == 'open_log_location':
            try:
                run_files_manager.run_explorer_sel(log_file_path)
            except:
                message: str = "Failed to open file manager"
                logger.error(message + "\n" + traceback.format_exc())
                sg.popup(message)
        elif event == 'copy_log_path':
            logger.info("Copying log path to clipboard.")
            sg.clipboard_set(str(log_file_path))
        elif maps_loading_interaction_manager.handle_event(event):
            pass
        else:
            logger.error("GUI event not handled")
except:
    fe: str = traceback.format_exc()
    logger.fatal("Unhandled exception:\n" + fe)
    sg.popup(f"\
FATAL ERROR OCCURED!\n\
Unhandled exception:\n{fe}\n\
You have discovered an OMSI Map Merger bug, app developer may not know about.\n\n\
App log is located in \"{log_file_path}\".\n\
You may like to grab it and share with other users/developers to help fix this issue.\n\n\
OMSI Map Merger will be terminated now.",
             title="Fatal error")
    logger.info("Program will be terminated due to fatal error.")

logger.info("Closing OMSI Map Merger")
window.close()
