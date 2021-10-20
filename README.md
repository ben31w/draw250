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

# Sample drawings
![draw250-blue-circles](https://user-images.githubusercontent.com/78334282/138126629-51e10338-da07-4284-a98e-cf9c423b5601.png)


![draw250-circles](https://user-images.githubusercontent.com/78334282/138127037-dad892ed-d2e5-46ba-8c82-9fa309aa8486.png)

![draw250-abstract-circles](https://user-images.githubusercontent.com/78334282/138127068-4309d0b7-def5-4c12-9020-4c5954925a9c.png)

![draw250-big-dipper](https://user-images.githubusercontent.com/78334282/138127107-01f19552-a094-4d4e-b227-4d4ce25fab9b.png)

![draw250-windows](https://user-images.githubusercontent.com/78334282/138127131-086ba56d-b7d2-4d8e-a839-d0422203c7a7.png)

All the drawings are saved as `.dwg` files. To open them, you must run `draw250.py` and select `Open` from the file menu.
