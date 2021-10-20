# Overview
This is a drawing program made using Tkinter. In this program, the user is given a blank canvas that they can draw circles, rectangles, etc. on, and the user can save and open their work as `.dwg` (binary) files. 

# Supported operations/functions
* `New` - clear canvas 
* `Open` - open a previously saved file
* `Save` - resave using the current file name
* `Save As` - select a new file name

The user can adjust the fill and edge color of the shapes they draw.

# File structure
The project contains several files to support the various shapes the user can draw: `shape.py`, `circle.py`, `ellipse.py`, `rectangle.py`, and `square.py`. Each file contains a class with the same name.

To use the program, run the file `draw250.py`.
