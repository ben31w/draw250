from src.invalid_shape_parameter_error import InvalidShapeParameterError
from src.shape import Shape


class Circle(Shape):

    def __init__(self, x, y, radius=None, fill_color='', edge_color='red', dash_style=None, dx=None, dy=None):

        super().__init__(x, y, fill_color, edge_color, dash_style, dx, dy)

        # If radius is not given, but dx and dy are (dx and dy are the mouse's
        # distance from the center in terms of x and y, respectively), make radius
        # the max between dx and dy.
        if radius is None and dx is not None and dy is not None:
            radius = max(dx, dy)

        if radius is None:
            raise InvalidShapeParameterError("Circle: radius not defined!")

        self.x_axis = radius
        self.y_axis = radius
        self.radius = radius

    def __str__(self):
        """
        Return special string for circle
        :return:
        """
        return f"{Shape.__str__(self)} r={self.radius}"

    def draw(self, canvas):

        x0 = self.x - self.x_axis
        y0 = self.y - self.y_axis
        x1 = self.x + self.x_axis + 1  # (x1,y1) is just outside the oval
        y1 = self.y + self.y_axis + 1

        if self.tk_id is not None:
            canvas.delete(self.tk_id)

        self.tk_id = canvas.create_oval(x0, y0, x1, y1, fill=self.fill_color, outline=self.edge_color,
                                        dash=self.dash_style)

    def update(self, canvas, dx, dy, dash_style=(5, 5)):
        self.x_axis = dx
        self.y_axis = dy
        self.dash_style = dash_style
        x0 = self.x - self.x_axis
        y0 = self.y - self.y_axis
        x1 = self.x + self.x_axis + 1  # (x1,y1) is just outside the oval
        y1 = self.y + self.y_axis + 1
        # print(" Updating ",self.__class__.__name__," with ",dx,dy)

        if self.tk_id is not None:
            canvas.delete(self.tk_id)

        self.tk_id = canvas.create_oval(x0, y0, x1, y1,
                                        fill='',
                                        outline=self.edge_color,
                                        dash=self.dash_style)
