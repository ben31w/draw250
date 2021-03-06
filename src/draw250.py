# Code loosely based on the following open source projects:
# https://github.com/raspberrypilearning/shapes
# https://github.com/mozilla/stoneridge/blob/master/python/src/Demo/tkinter/matt/rubber-band-box-demo-1.py
# https://gist.github.com/nikhilkumarsingh/85501ee2c3d8c0cfa9d1a27be5781f06
"""
Draw250:
This a GUI program that allows you make and save your own drawings, as well as open previous drawings.
You can draw circles, ellipses, rectangles, and squares. You can save your work, open previous
drawings, and create blank canvases using the File menubar.

@author Ben Wright, Alaaeldin Haroun
@version 2021.09.03
"""
import os
import pickle

try:
    from tkinter import *
    from tkinter import filedialog
    from tkinter.colorchooser import askcolor
except ImportError:
    print("tkinter did not import successfully - check you are running Python 3 and that tkinter is available.")
    exit(1)

from circle import Circle
from ellipse import Ellipse
from square import Square
from rectangle import Rectangle


class Draw:

    def __init__(self, width, height):
        """
        Define the layout of the window, and set up the canvas.
        Initialize variables to store the shapes that the user draws, the name of the file they are working on,
        and whether their work is unsaved.
        :param width: the width of the frame in pixels
        :param height: the height of the frame in pixels
        """
        self.shapes = list()
        self.file_name = None
        self.unsaved = False
        self.new_shape = None

        # Set up the root window
        self.root = Tk()
        self.set_root_title()

        # Define our layout grid
        self.grid = Frame(self.root)
        self.grid.grid_columnconfigure(7, weight=1)
        self.grid.grid_rowconfigure(3, weight=1)

        # Top level menu buttons
        self.file_mb = Menubutton(self.grid, text='File')
        self.file_mb.grid(row=0, column=0, sticky=W)
        self.file_mb.menu = Menu(self.file_mb)
        self.file_mb['menu'] = self.file_mb.menu
        # Add the commands to the file menubutton
        self.file_mb.menu.add_command(label='New', command=lambda: [self.clear_canvas(), self.reset_file_name()])
        self.file_mb.menu.add_command(label='Open', command=self.browse_files)
        self.file_mb.menu.add_command(label='Save', command=self.save_file_dialog)
        self.file_mb.menu.add_command(label='Save As', command=self.save_as_file_dialog)
        self.file_mb.menu.add_separator()
        self.file_mb.menu.add_command(label='Exit', command=quit)

        # Shape choice menu
        available_shapes = ['Circle', 'Ellipse', 'Rectangle', 'Square']  # list of shapes available
        self.shape_choice = StringVar(self.root)  # Initialize string to hold value
        self.shape_choice.set(available_shapes[0])  # default value

        self.shape_choice_menu = OptionMenu(self.grid, self.shape_choice, *available_shapes)
        self.shape_choice_menu.grid(row=1, column=1)

        # Shape fill color and box check
        self.fill_color = 'blue'
        self.prior_fill_color = 'blue'

        self.fill_check = BooleanVar(self.root, value=True)
        self.fill_check_box = Checkbutton(self.grid, text='fill', variable=self.fill_check, command=self.fill_toggle)
        self.fill_check_box.grid(row=1, column=2, sticky=E)
        self.fill_check_box.select()  # Start checked by default

        self.fill_color_button = Button(self.grid, text='fill color', command=self.choose_fill_color)
        self.fill_color_button.grid(row=1, column=3, sticky=E)

        self.fill_canvas = Canvas(self.grid, background=self.fill_color, width=15, height=15)
        self.fill_canvas.grid(row=1, column=4, sticky=W)

        # Edge Color
        self.edge_color = 'red'
        self.prior_edge_color = 'red'

        self.edge_color_button = Button(self.grid, text='edge color', command=self.choose_edge_color)
        self.edge_color_button.grid(row=1, column=5, sticky=E)

        self.edge_canvas = Canvas(self.grid, background=self.edge_color, width=15, height=15)
        self.edge_canvas.grid(row=1, column=6, sticky=W)

        # The Canvas
        self.canvas = Canvas(self.grid, background='white', width=width, height=height)
        self.canvas.grid(row=2, column=0, columnspan=7)

        self.canvas.bind("<Button-1>", self.select)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        self.grid.pack()

    def shape_selection(self):
        """
        returns the shape the user selected
        :return: The shape selected from the list
        """
        if self.shape_choice.get() == "Circle":
            return Circle
        elif self.shape_choice.get() == "Ellipse":
            return Ellipse
        elif self.shape_choice.get() == "Square":
            return Square
        elif self.shape_choice.get() == "Rectangle":
            return Rectangle

    def add_shape(self, shape):
        """Add a shape to the list of shapes."""
        print("\tAdding ", shape)
        self.shapes.append(shape)
        self.unsaved = True

    def browse_files(self):
        """
        Open a file explorer and prompt the user to select a DWG file to open.
        """
        self.file_name = filedialog.askopenfilename(defaultextension='.dwg',
                                                    initialdir=os.path.join("Desktop", "cpsc250l",
                                                                            "cpsc250l-lab12-f20"),
                                                    title="Select a File",
                                                    filetypes=(("DWG files", "*.dwg*"), ("all files", "*.*")))
        self.set_root_title()
        self.load_shapes(self.file_name)

    def choose_fill_color(self):
        """Sets the shape fill color"""
        get_color = askcolor(color=self.fill_color)
        print(" get_color=", get_color)
        self.fill_color = get_color[1]
        self.fill_canvas.configure(background=self.fill_color)
        self.prior_fill_color = self.fill_color
        self.fill_check_box.select()  # Selecting color automatically selects fill

    def choose_edge_color(self):
        """Sets the shape's edge color"""
        get_color = askcolor(color=self.edge_color)
        print(" get_color=", get_color)
        self.edge_color = get_color[1]
        self.edge_canvas.configure(background=self.edge_color)
        self.prior_edge_color = self.edge_color

    def clear_canvas(self):
        """Clear the canvas and remove all shapes."""
        self.shapes.clear()
        self.repaint()

    def drag(self, event):
        """
        A "rubber band" that we stretch to define the shape extents
        :param event:
        :return:
        """
        dx = abs(self.new_shape.x - event.x)
        dy = abs(self.new_shape.y - event.y)
        self.new_shape.update(self.canvas, dx, dy, dash_style=(5, 5))

    def fill_toggle(self):
        print(" fill checkbox  ", self.fill_check.get())
        if self.fill_check.get():
            self.fill_color = self.prior_fill_color
        else:
            self.fill_color = ''

    def load_shapes(self, filename):
        """
        Given a binary filename with a list of shapes (i.e., a DWG file), load
        the shapes from that file onto the canvas.
        :param filename: a binary file with a list of shapes
        """
        # Clear the canvas before loading shapes.
        self.clear_canvas()

        # Load the file and put the shapes on the canvas.
        self.shapes = pickle.load(open(filename, 'rb'))
        for shape in self.shapes:
            shape.draw(self.canvas)

        # The newly opened file should not have unsaved work.
        self.unsaved = False

    def release(self, event):
        """
        On release, we create the shape and add to list of shapes
        :param event:
        :return:
        """
        print("\tRelease: ", event.x, event.y)
        dx = abs(self.new_shape.x - event.x)
        dy = abs(self.new_shape.y - event.y)

        self.canvas.delete(self.new_shape.tk_id)

        print("\tCompleting ", self.shape_choice.get(), "!")
        cls = self.shape_selection()
        self.add_shape(cls(self.new_shape.x, self.new_shape.y,
                           dx=dx, dy=dy, fill_color=self.fill_color,
                           edge_color=self.edge_color))
        self.repaint()
        self.new_shape = None

    def repaint(self):
        print("\tRepaint the canvas")
        self.canvas.delete("all")

        for shape in self.shapes:
            shape.draw(self.canvas)

        print("\tDone repainting!")

    def reset_file_name(self):
        """Reset the current file to None."""
        self.file_name = None
        self.set_root_title()

    def run(self):
        print("inside Draw run loop ...")
        self.root.mainloop()
        print("done running!")

    def save_as_file_dialog(self):
        """Opens a save as dialog box and lets the user save a file."""
        self.file_name = filedialog.asksaveasfilename(initialdir=".", title="Select file",
                                                      filetypes=(("drawing files", "*.dwg"), ("all files", "*.*")))
        if self.file_name is not None and len(self.file_name) > 0:
            self.save_shapes()

    def save_file_dialog(self):
        """Saves the user's work."""
        if self.file_name is None:
            self.save_as_file_dialog()
        else:
            self.save_shapes()

    def save_shapes(self):
        """Save the shapes to a binary file."""
        try:
            pickle.dump(self.shapes, open(self.file_name, "wb"))
            self.unsaved = False
            self.set_root_title()
        except Exception as e:
            print(e)
            print("Cannot save shapes")

    def select(self, event):
        """
        On select (button press) we create a temporary shape used to
        draw the stretchy "rubber band" used to define the extents
        :param event:
        :return:
        """
        print("\tCreating ", self.shape_choice.get(), " at (", event.x, ", ", event.y, ")")
        cls = self.shape_selection()
        print("\t class : ", cls.__name__)
        print("\t fill=", self.fill_color, ' edge=', self.edge_color)
        self.new_shape = cls(event.x, event.y, dx=0, dy=0,
                             fill_color=self.fill_color,
                             edge_color=self.edge_color)

    def set_root_title(self):
        """Set the title of the root window."""
        if self.file_name is not None:
            self.root.title(f"Draw 250 - {self.file_name}")
        else:
            self.root.title(f"Draw 250 - untitled work")


if __name__ == '__main__':
    draw = Draw(800, 600)

    draw.repaint()
    draw.run()
    print("Done run loop - call save_shapes ...")

    print("Done drawing!")
