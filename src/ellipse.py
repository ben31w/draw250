from src.invalid_shape_parameter_error import InvalidShapeParameterError
from src.shapes import Shape


class Ellipse(Shape):
    def __init__(self, x, y, height=None, width=None, fill_color='', edge_color='red', dash_style=None, dx=None,
                 dy=None, ):
        super().__init__(x, y, fill_color, edge_color, dash_style, dx, dy)

        if height is None and width is None and dx is not None and dy is not None:
            height = dy*2
            width = dx*2

        if height is None or width is None:
            raise InvalidShapeParameterError("Ellipse is not defined!!")

        self.x_axis = width/2
        self.y_axis = height/2
        self.height = height
        self.width = width

    def __str__(self):
        """
        Return special string for circle, not based on ellipse
        :return:
        """
        return f"{Shape.__str__(self)} w={self.width} h={self.height}"

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