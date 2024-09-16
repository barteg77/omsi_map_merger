# User Manual

1. Start by going to the **"Reading maps files"** section on the left side. Add maps one by one using the **"Add"** button.
2. Press **"Read whole maps"** to load the maps. This will take some time, and the program will not respond until completion of read.
3. When the program becomes responsive again, see to what extent the maps have been loaded. If all entries in the table have a value of **True** in the **Ready** column, proceed to the next step.
Otherwise, expand the tree structure of the loaded map by clicking the triangle on the left side to see what the issue is.
   - Each element in the tree represents an object of one of the following types:
     - **unit** - a single file of OMSI map
     - **list** - a group of lists and/or units
   - After selecting an element, detailed error information (if any) will be displayed below the tree.
   - For each element, you can use the **Load selected** option to retry loading (e.g., after fixing the file).
   - For unit-type elements, you can use the **Open file in editor** option, which will open the file in your default editor.
   - For OmsiMap-type elements, if **global.cfg** is loaded, you can use the **Scan for chronos** option, which will search for chrono directories.
   - For Timetable-type elements, you can use the **Scan for lines**, **Scan for tracks**, and **Scan for trips** options, which will search for **ttl**, **ttr**, and **ttp** files in the given timetable.
4. After selecting a map (not its subordinate elements) in the table, you can move it using buttons below the diagram. Arrange the maps as you wish.
5. After selecting a map in the table as mentioned above, the button **(toggle) Keep original main ground texture on tiles of selected map** becomes active. You can use it to apply a ground texture covering the entire area of the selected map, imitating different main ground texture on this area. State of this option is indicated on the diagram by an **X** on the tiles of the selected map.
6. Choose the directory where the merged map will be saved.
7. Enter the name of the new map (it will be displayed when selecting the map in OMSI).
8. Press **Merge maps!**
9. If there are warnings, you will be informed about them and will have the option to cancel the map saving. If you do not cancel, the map will be saved.
10. There is an option to reload the map or its parts, move it, etc., and then save the map again.
